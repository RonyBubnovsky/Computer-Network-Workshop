# P2P RTT Project (TCP Communication)

This project implements a peer-to-peer (P2P) application for measuring Round-Trip Time (RTT) between nodes using TCP socket programming in Python.

## Table of Contents
- [Overview](#overview)
- [Server Side](#server-side)
- [Client Side](#client-side)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)

## Overview

The P2P RTT project facilitates communication and RTT measurement among multiple servers and clients over a local network using TCP.

## Server Side

The server side of the project includes functionalities such as:
- Establishing TCP connections with other servers and clients.
- Handling requests to join a clique of connected servers.
- Broadcasting and forwarding messages between clients within the same server or across connected servers.
- Calculating minimal RTT and optimizing connections based on network performance.

Key functions:
- `ask_for_clique(connect_sock, port_to_add_to_dict, port)`: Requests and processes information about the clique of connected servers.
- `connect_to_servers_in_the_clique(clique_ports, my_port)`: Establishes TCP connections with other servers in the received clique.
- Handlers for various message types (`handle_clique_request`, `handle_new_connection_from_client`, `handle_messages`, etc.) that manage communication protocols and data exchange.

## Client Side

The client side involves:
- Connecting via TCP to a specified server.
- Sending and receiving messages with other clients connected to the same server or across the network through connected servers.
- Calculating and selecting minimal RTT for optimal communication.

Key functions:
- `calculate_minimal_port(minimal_socket)`: Determines the server with the minimal RTT and establishes the TCP connection.
- `connect_client_to_server(minimal_socket)`: Initiates a TCP connection to the selected server and manages client registration.
- `wait_for_messages(minimal_socket)`: Monitors incoming messages from other clients and displays them.

## Setup

Ensure Python 3.x is installed on your system. No additional libraries are required beyond the standard Python socket and struct modules.

## Usage

1. Clone the repository and navigate to the project directory.
2. Start the server by running `python server.py`.
3. Start a client by running `python client.py`.
4. Follow the prompts to select ports and initiate TCP connections.
5. Communicate between clients by entering messages in the format `<client_name> <message>`.

## Contributing

Contributions to enhance functionality or fix issues are welcome. Fork the repository, create a new branch, make your changes, and submit a pull request.
