# TCP P2P Project

This project demonstrates a Peer-to-Peer (P2P) communication system using Transmission Control Protocol (TCP). The system includes functionalities for servers to form and maintain a clique (a group of interconnected servers) and for clients to connect to these servers to send and receive messages.

## Overview

### Server Side

The server script allows multiple servers to connect, form a clique, and exchange information about connected clients and messages. Key functionalities include:

- **Clique Formation**: Servers connect to each other, exchange clique information, and maintain connections within the clique.
- **Client Management**: Servers manage connected clients, including adding new clients, forwarding messages between clients within the server, and broadcasting messages to clients connected to other servers in the clique.

### Client Side

The client script allows users to connect to a specified server within the clique, register a name, and send messages to other clients within the server or broadcast messages to clients connected to other servers in the clique. Key functionalities include:

- **Connection Setup**: Clients connect to a chosen server within the clique and register their name.
- **Message Exchange**: Clients can send messages directly to clients within the same server or broadcast messages to clients across the clique.

## Prerequisites

- Basic understanding of networking concepts, including TCP/IP and socket programming.
- Python installed on your local machine.

## How to Run

1. Save the server-side code in a file, e.g., `server_tcp_p2p.py`, and the client-side code in another file, e.g., `client_tcp_p2p.py`.
2. Start the server script:
    ```sh
    python server_tcp_p2p.py
    ```
3. Choose an index from the available ports when prompted.
4. Start the client script in a separate terminal session:
    ```sh
    python client_tcp_p2p.py
    ```
5. Enter the index of the port you want to connect to when prompted.

### Sample Run

1. When the server script runs, it will prompt you to choose a port index:
    ```
    Choose an index [0-4] :
    ```
2. Enter an index (e.g., `0` for the first port in the list).
3. The server will start listening on the chosen port and attempt to connect to other servers in the specified ports.
4. When the client script runs, it will prompt you to enter an index of the port to connect to:
    ```
    Enter index port to connect to [0-4]:
    ```
5. Enter an index (e.g., `0` for the first port in the list).
6. The client will connect to the specified server and prompt you to enter your name.
7. You can then send messages in the format `<client_name> <message>` to communicate with other clients.

## Summary

This project provides a practical implementation of a TCP-based Peer-to-Peer communication system. It demonstrates how servers can form and manage cliques dynamically and how clients can interact within this P2P network to send and receive messages.

Feel free to explore and modify the code to further understand the concepts of P2P communication and network programming.
