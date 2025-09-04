import socket
import threading
import requests
import json
import os
import re

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 5000        # Port to listen on
USER_FILE = "users.json"

# Open Library API base URL
OPEN_LIBRARY_API = "https://openlibrary.org/search.json"


if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({"users": {}}, f)

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=4)

def authenticate_user(conn):
    conn.sendall(b"Enter username: ")
    username = conn.recv(1024).decode('utf-8').strip()
    conn.sendall(b"Enter password: ")
    password = conn.recv(1024).decode('utf-8').strip()

    users = load_users()
    if username in users["users"] and users["users"][username]["password"] == password:
        conn.sendall(b"Authentication successful!\n")
        return username
    else:
        conn.sendall(b"Authentication failed. Goodbye!\n")
        return None

def register_user(conn):
    conn.sendall(b"Enter a new username: ")
    username = conn.recv(1024).decode('utf-8').strip()
    conn.sendall(b"Enter a new password: ")
    password = conn.recv(1024).decode('utf-8').strip()

    users = load_users()
    if username in users["users"]:
        conn.sendall(b"Username already exists.\n")
    else:
        users["users"][username] = {"password": password, "history": []}
        save_users(users)
        conn.sendall(b"Registration successful! You can now log in.\n")

def search_books(query):
    """Search for books using Open Library's API with a fallback."""
    fallback_data = [
        {"title": "Pride and Prejudice", "author_name": ["Jane Austen"]},
        {"title": "1984", "author_name": ["George Orwell"]},
        {"title": "To Kill a Mockingbird", "author_name": ["Harper Lee"]},
        {"title": "Moby Dick", "author_name": ["Herman Melville"]},
        {"title": "The Great Gatsby", "author_name": ["F. Scott Fitzgerald"]},
    ]

    try:
        response = requests.get(OPEN_LIBRARY_API, params={"q": query, "limit": 10}, timeout=5)
        response.raise_for_status()
        data = response.json()
        books = data.get("docs", [])
        if not books:
            return ["No books found for the given query."]
        return [f"{idx + 1}. {book.get('title', 'Unknown Title')} by {book.get('author_name', ['Unknown Author'])[0]}" for idx, book in enumerate(books)]
    except requests.exceptions.RequestException:
        # Use fallback data if API fails
        filtered_books = [book for book in fallback_data if query.lower() in book["title"].lower()]
        if not filtered_books:
            return [f"API unavailable. No local results found for '{query}'."]
        return [f"API unavailable. Showing local results for '{query}'"] + [
            f"{idx + 1}. {book['title']} by {book['author_name'][0]}" for idx, book in enumerate(filtered_books)
        ]

def is_valid_book_title(title): 
    return re.match(r'^[A-Za-z0-9\s]+$', title) is not None

def handle_client(conn, addr):
    print(f"New connection from {addr}")

    try:
        while True:
            request = conn.recv(1024).decode('utf-8').strip()
            print(f"Received from client: {request}")

            if request.lower() == "register":
                register_user(conn)
            elif request.lower() == "login":
                username = authenticate_user(conn)
                if username:
                    while True:
                        try:
                            request = conn.recv(1024).decode('utf-8').strip()
                            print(f"Received command from client: {request}")

                            if "|" in request:
                                cmd, value = request.split("|", 1)
                                cmd = int(cmd)
                            else:
                                cmd, value = int(request), None

                            if cmd == 1:  # Search
                                if value:
                                    response = "\n".join(search_books(value))
                                else:
                                    response = "Provide a search query.\n"
                                conn.sendall(response.encode('utf-8'))  
                                
                            elif cmd == 2:  # Borrow a book
                                if value and is_valid_book_title(value):
                                    users = load_users()
                                    user_history = users["users"][username]["history"]

                                    # Check if the book is already borrowed
                                    all_borrowed_books = [entry["book"] for entry in user_history if entry["action"] == "borrowed"]
                                    if value not in all_borrowed_books:
                                        user_history.append({"action": "borrowed", "book": value})
                                        save_users(users)
                                        response = f"You have borrowed '{value}'."
                                    else:
                                        response = f"'{value}' is already borrowed."
                                else:
                                    response = "Invalid book title."
                                conn.sendall(response.encode('utf-8'))

                            elif cmd == 3:  # Return a book
                                if value and is_valid_book_title(value):
                                    users = load_users()
                                    user_history = users["users"][username]["history"]

                                    # Check if the user has borrowed this book
                                    borrowed_books = [entry["book"] for entry in user_history if entry["action"] == "borrowed"]
                                    if value in borrowed_books:
                                        user_history.append({"action": "returned", "book": value})
                                        save_users(users)
                                        response = f"Returned '{value}'."
                                    else:
                                        response = f"'{value}' was not borrowed by you."
                                else:
                                    response = "Invalid book title."
                                conn.sendall(response.encode('utf-8'))

                            elif cmd == 4:  # View history
                                users = load_users()
                                user_history = users["users"][username]["history"]

                                # Format the history for display
                                if user_history:
                                    history_entries = [f"{entry['action'].capitalize()}: {entry['book']}" for entry in user_history]
                                    response = "\n".join(history_entries)
                                else:
                                    response = "No history available."

                                conn.sendall(response.encode('utf-8'))  # Send response immediately

                            elif cmd == 5:  # Exit from subcommand menu
                                response = "Logged out successfully. Returning to the main menu.\n\nWelcome to the Library Client! \nCommands:\n1: Register\n2: Login\n3: Exit\n"
                                conn.sendall(response.encode('utf-8'))
                                print(f"Processed command {cmd} (Logout) from {addr}")
                                handle_client(conn, addr)
                                

                            # Send response to the client
                            conn.sendall(response.encode('utf-8'))

                            # Log only the command, not the response
                            print(f"Processed command {cmd} from {addr}")

                        except Exception as e:
                            conn.sendall(f"Error processing command: {e}".encode('utf-8'))
                            break

                break
            else:
                conn.sendall(b"Invalid command. Use 'register' or 'login'.\n")

    except Exception as e:
        print(f"Error: {e}")
        conn.sendall(f"Error: {e}".encode('utf-8'))
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server running on {HOST}:{PORT}...")

        while True:
            conn, addr = server.accept()
            print(f"New connection from {addr}")
            conn.sendall(b"Welcome to the library server! Please enter 'register' or 'login'.\n")

            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"Active connections: {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
