# Basic TCP Project

This project demonstrates the implementation of a basic Transmission Control Protocol (TCP) communication. A single script is used to set up both server and client functionalities, allowing the server to listen for incoming connections and attempt to connect to other servers on specified ports.

## Overview

### Functionality

- **Server Setup**: The script sets up a TCP server that listens on a specified port from a list of available ports.
- **Client Setup**: Concurrently, the script attempts to connect to other servers on the remaining ports in the list.
- **Communication**: When a connection is established between servers, they exchange messages.

### Key Components

- **Port Selection**: The user selects a port from a predefined list.
- **Server Listening**: The server listens for incoming connections on the chosen port.
- **Client Connection**: The client attempts to connect to other servers on different ports.
- **Message Exchange**: Servers exchange simple "Hello" and "World" messages upon connection.

## How to Run

1. Save the code in a file, e.g., `basic_tcp.py`.
2. Run the script:
    ```sh
    python basic_tcp.py
    ```
3. Choose an index from the available ports when prompted.

### Sample Run

1. When the script runs, it will prompt you to choose a port index:
    ```
    Choose an index [0-4]:
    ```
2. Enter an index (e.g., `0` for the first port in the list).
3. The server will start listening on the chosen port and attempt to connect to other servers on the remaining ports.

## Summary

This project provides a basic understanding of TCP communication by demonstrating how a single script can function both as a server and a client. It showcases setting up TCP connections, handling multiple connections using threads, and simple message exchanges between servers.

Feel free to explore and modify the code to further understand the concepts of TCP communication.
