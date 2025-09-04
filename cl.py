import socket
import time

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 5000         # Port to connect to

def start_client():
    print("Welcome to the Library Client!")
    print("Commands:")
    print("1: Register")
    print("2: Login")
    print("3: Exit\n")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((HOST, PORT))
            print("Connected to the server.")

            # Read and display the welcome message
            welcome_message = client.recv(1024).decode('utf-8')
            print(f"{welcome_message.strip()}")

            while True:
                command = input("Enter command number: ").strip()
                if command == "1":  # Register
                    client.sendall("register".encode('utf-8'))
                    print(client.recv(1024).decode('utf-8'))  # Enter username
                    username = input("Username: ").strip()
                    client.sendall(username.encode('utf-8'))

                    print(client.recv(1024).decode('utf-8'))  # Enter password
                    password = input("Password: ").strip()
                    client.sendall(password.encode('utf-8'))

                    # Registration response
                    print(client.recv(1024).decode('utf-8'))

                elif command == "2":  # Login
                    client.sendall("login".encode('utf-8'))
                    print(client.recv(1024).decode('utf-8'))  # Enter username
                    username = input("Username: ").strip()
                    client.sendall(username.encode('utf-8'))

                    print(client.recv(1024).decode('utf-8'))  # Enter password
                    password = input("Password: ").strip()
                    client.sendall(password.encode('utf-8'))

                    # Login response
                    response = client.recv(1024).decode('utf-8')
                    print(f"{response}")

                    if "successful" in response:
                        while True:
                            print("Available commands:")
                            print("1: Search for books")
                            print("2: Borrow a book")
                            print("3: Return a book")
                            print("4: View history")
                            print("5: Exit")
                            subcommand = input("Enter command number: ").strip()

                            if subcommand == "1":  # Search for books
                                query = input("Enter search query: ").strip()
                                client.sendall(f"1|{query}".encode('utf-8'))
                                
                                # Receive and display server response
                                response = client.recv(1024).decode('utf-8')
                                print("\nSearch results:\n")
                                print(f"{response.strip()}\n")  
                                
                            elif subcommand == "2":  # Borrow a book
                                book = input("Enter the book title to borrow: ").strip()
                                client.sendall(f"2|{book}".encode('utf-8'))

                                # Display the server's response immediately
                                response = client.recv(1024).decode('utf-8')
                                print(f"\n{response.strip()}\n")

                            elif subcommand == "3":  # Return a book
                                book = input("Enter the book title to return: ").strip()
                                client.sendall(f"3|{book}".encode('utf-8'))

                                # Display the server's response immediately
                                response = client.recv(1024).decode('utf-8')
                                print(f"\n{response.strip()}\n")

                            elif subcommand == "4":  # View history
                                client.sendall("4".encode('utf-8'))

                                # Wait for and display the history response from the server
                                time.sleep(0.1)  # Small delay to ensure server flushes buffer
                                response = client.recv(1024).decode('utf-8')
                                print("\nHistory:\n")
                                print(response.strip())
                                print("\n")  # Add a new line for clarity

                            elif subcommand == "5":  # Logout
                                client.sendall("5".encode('utf-8'))
                                print("Logging out...")
                                try:
                                    # Receive server confirmation
                                    logout_message = client.recv(1024).decode('utf-8')
                                    print(logout_message)
                                except ConnectionResetError:
                                    print("The server closed the connection unexpectedly.")
                                break



                            else:
                                print("Invalid command. Please enter a number between 1 and 5.")
                                continue

                elif command == "3":  # Exit
                    client.sendall("3".encode('utf-8'))  # Send exit command to server
                    print("Disconnected from the server. You can reconnect if needed.")
                    break  # Exit the client loop

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    start_client()
