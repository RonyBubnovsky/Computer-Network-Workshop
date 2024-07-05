# Basic UDP Project

This project demonstrates the implementation of a basic User Datagram Protocol (UDP) communication between a server and multiple clients. The server manages user registrations and message forwarding based on usernames.

## Overview

### Server Side

The server listens for incoming UDP packets, registers new clients, and forwards messages to the intended recipients. It handles:

- Client registration with unique usernames.
- Message forwarding to the correct client based on the username.
- Error handling for invalid messages and duplicate usernames.

### Client Side

The client registers with the server using a unique username and allows the user to send messages to other registered clients. It handles:

- Sending the username to the server for registration.
- Sending messages to other clients through the server.
- Receiving messages from the server.

## How to Run

### Server

1. Save the server code in a file, e.g., `udp_server.py`.
2. Run the server code:
    ```sh
    python udp_server.py
    ```

### Client

1. Save the client code in a file, e.g., `udp_client.py`.
2. Run the client code:
    ```sh
    python udp_client.py
    ```
3. Enter your name when prompted.
4. Type messages in the format `username message` to send a message to another user.

## Summary

This project provides a basic understanding of UDP communication and demonstrates how to manage client registrations and message forwarding using UDP sockets.

Feel free to explore and modify the code to further understand the concepts of UDP communication.
