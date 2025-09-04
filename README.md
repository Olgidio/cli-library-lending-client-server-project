This is a client server project using python principles to simulate a library lending system. 
Contents

    Directory Structure
    Submission Guidelines
    Building and Running Instructions
    Application Features


Directory Structure
    Client code file
    Server code file
    SSL certificate (server.crt) and private key (server.key).
    Implementation log file
    Features Checklist file
    This README file

Submission Guidelines
Prerequisites

    Python Version: Ensure Python 3.8 or later is installed.
    Ensure all files (.py, .cnf, .crt,.csr,.key) are in the same directory
    Required Libraries:
        requests: Install with pip install requests.
        Other libraries (socket, threading, json, ssl, etc.) are part of the Python standard library.
    Certificates:
        Ensure server.crt and server.key are in the same directory as server.py for SSL encryption.

Running the Application

    Start the Server:
        Open the terminal (e.g. CMD) and navigate to the server directory.
        Run the server script:
            python server.py
        The server will start and listen for incoming connections.

        Run the client script:
            python client.py

        Follow the on-screen instructions to interact with the library system.

Application Features
Core Features

    User Authentication:
        Users can register with a username and password.
        Passwords are hashed for secure storage.
        Users can log in to access library features.
    Book Search:
        Real-time search functionality using the Open Library API.
    Borrow and Return Books:
        Users can borrow and return books.
        Borrowing history is maintained for each user.
    History Tracking:
        Users can view their borrowing history.

Security Features

    SSL/TLS Encryption:
        All communication between client and server is encrypted.
        A self-signed certificate (server.crt) is used for secure connections. (this is not included in the public repo.)
