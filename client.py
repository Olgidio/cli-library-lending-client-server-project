import socket
import ssl
import time

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 5000         # Port to connect to

def start_client():
    print("Welcome to the Library Client!")


    # Set up SSL
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False  # Disable hostname check for local testing
    context.load_verify_locations("server.crt")  # Load the server's certificate

    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=HOST) as secure_client:
            print("Connected to the secure server.")

            # Read and display the welcome message
            welcome_message = secure_client.recv(1024).decode('utf-8')
            print(f"{welcome_message.strip()}")

            while True:
                command = input("1. Register\n2. Login\n3. Exit\nEnter command number:\n").strip()
                if command == "1":  # Register
                    secure_client.sendall("register".encode('utf-8'))
                    print(secure_client.recv(1024).decode('utf-8'))  # Enter username
                    username = input("Username: ").strip()
                    secure_client.sendall(username.encode('utf-8'))

                    print(secure_client.recv(1024).decode('utf-8'))  # Enter password
                    password = input("Password: ").strip()
                    secure_client.sendall(password.encode('utf-8'))

                    # Registration response
                    print(secure_client.recv(1024).decode('utf-8'))

                elif command == "2":  # Login
                    secure_client.sendall("login".encode('utf-8'))
                    print(secure_client.recv(1024).decode('utf-8'))  # Enter username
                    username = input("Username: ").strip()
                    secure_client.sendall(username.encode('utf-8'))

                    print(secure_client.recv(1024).decode('utf-8'))  # Enter password
                    password = input("Password: ").strip()
                    secure_client.sendall(password.encode('utf-8'))

                    # Login response
                    response = secure_client.recv(1024).decode('utf-8')
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
                                secure_client.sendall(f"1|{query}".encode('utf-8'))

                                # Receive and display server response
                                response = secure_client.recv(1024).decode('utf-8')
                                print("\nSearch results:\n")
                                print(f"{response.strip()}\n")

                            elif subcommand == "2":  # Borrow a book
                                book = input("Enter the book title to borrow: ").strip()
                                secure_client.sendall(f"2|{book}".encode('utf-8'))

                                # Display the server's response immediately
                                response = secure_client.recv(1024).decode('utf-8')
                                print(f"\n{response.strip()}\n")

                            elif subcommand == "3":  # Return a book
                                book = input("Enter the book title to return: ").strip()
                                secure_client.sendall(f"3|{book}".encode('utf-8'))

                                # Display the server's response immediately
                                response = secure_client.recv(1024).decode('utf-8')
                                print(f"\n{response.strip()}\n")

                            elif subcommand == "4":  # View history
                                secure_client.sendall("4".encode('utf-8'))
                                response = secure_client.recv(1024).decode('utf-8')
                                print("\nHistory:\n")
                                print(response.strip())
                                print("\n")  

                            elif subcommand == "5":  # Logout
                                secure_client.sendall("5".encode('utf-8'))
                                print("Logging out...")
                                try:
                                    logout_message = secure_client.recv(1024).decode('utf-8')
                                    print(logout_message)
                                except ConnectionResetError:
                                    print("The server closed the connection unexpectedly.")
                                break

                elif command == "3":  # Exit
                    secure_client.sendall("3".encode('utf-8'))
                    print("Disconnected from the server")
                    break

if __name__ == "__main__":
    start_client()
