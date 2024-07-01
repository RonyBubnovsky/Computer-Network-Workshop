import socket
import struct
import threading


def ask_for_clique(connect_sock, port_to_add_to_dict, port):
    data = struct.pack('>bbhh', 0, 0, 0, 0)
    print("Request to get the clique packed\n")
    
    connect_sock.send(data)
    connect_sock.send(str(port_to_add_to_dict).encode())
    print("Request to get the clique sent\n")
    
    returned_data = connect_sock.recv(6)
    print("Received first 6 bytes of clique answer\n")
    
    type, subtype, length, sublen = struct.unpack('>bbhh', returned_data)
    if type == 1 and subtype == 0: # Answer from the server. receiving the clique.
        unpacked_data = connect_sock.recv(length)
        print("Received the clique data\n")
        print("The clique:", unpacked_data.decode(), '\n')
        
        splitted_clique = unpacked_data.decode().split('\0')
        only_ports = []
        for address in splitted_clique:
            only_ports.append(int(address.split(':')[1]))
        print(f"The clique Ports recieved from {port}: {only_ports}\n")
        
        return only_ports
         
def connect_to_servers_in_the_clique(clique_ports, my_port):
    count_connections = 0
    for port in clique_ports:
        if port != my_port: # every server in the clique except myself
            connect_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            connect_sock.connect(('127.0.0.1', port))
            print(f"{chosen_port} connected to {port} successfully Through Clique\n")
            servers_im_connected_to[port] = connect_sock # add a new connection to my dictionary of connections
            count_connections += 1
            connect_sock.send(struct.pack('>bbhh', 2, 0, 0, 0)) # Update the clique of the server i connected to
            connect_sock.send(str(my_port).encode()) # Send my port to the server i connected to
    if count_connections == 0 :
        print("No other server is in the clique")
                        
def try_connecting_to_other_servers():
    found_listening_server = False
    for port in ports_list:
        if port != chosen_port and not found_listening_server:
            try:
                connect_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) 
                connect_sock.connect(('127.0.0.1', port))
                print(f"{chosen_port} connected to {port} successfully. requesting from {port} its connected servers list...\n")
                servers_im_connected_to[port] = connect_sock
                print("FIRST SOCEKT:\n", connect_sock)
                connect_sock.send(struct.pack('>bbhh', 2, 0, 0, 0)) # Update the clique of the server i connected to
                connect_sock.send(str(chosen_port).encode()) # Send my port to the server i connected to
                clique_ports = ask_for_clique(connect_sock, chosen_port, port) # Ask for the clique of the other server
                connect_to_servers_in_the_clique(clique_ports, chosen_port) # Connect to the other servers in the received clique
                found_listening_server = True
            except ConnectionRefusedError:
                print(f"No server is listening on port {port}")
  
def handle_clique_request(conn_socket, client_address):
    print("Request to send clique unpacked\n")
    port_to_add = conn_socket.recv(4) # the port i need to add to my dict
    sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock3.connect(('127.0.0.1', int(port_to_add.decode())))
    servers_im_connected_to[int((port_to_add.decode()))] = sock3 # add the port that connects to me to my dict
    ip_and_ports_string = ""
    if len(servers_im_connected_to) > 0:
        for port in servers_im_connected_to.keys():
            ip_and_ports_string += '127.0.0.1' + ':' + str(port) + '\0'
        data_to_unpack = struct.pack('>bbhh', 1, 0, len(ip_and_ports_string)-1, 0)
        print("Clique packed\n")
        conn_socket.send(data_to_unpack)
        conn_socket.send(ip_and_ports_string[:-1].encode())
        print("Clique sent\n")         

def forward_message_between_clients_in_the_same_server(receiver, actual_message, conn_socket):
    print(f"{receiver} is connected to this server. Forwarding message to {receiver} ...\n")
    for client, socket in connected_clients.items():
        if socket == conn_socket: # Finding the source client
            message_to_send = client +'\0' + receiver + ' ' + actual_message
            sublength = len(client +'\0' + receiver)
            data = struct.pack('>bbhh', 3,0, len(message_to_send), sublength)
            connected_clients[receiver].send(data)
            connected_clients[receiver].send(message_to_send.encode()) 


def broadcast_message(receiver, actual_message, conn_socket):
    print(f"{receiver} is not connected to this server. Broadcasting message to other servers in the clique...\n")
    for client, socket in connected_clients.items():
        if socket == conn_socket: # Finding the source client
            sender = client 
    print("The ports i need to broadcast to are: ", list(servers_im_connected_to.keys()), '\n')
    for port in servers_im_connected_to.keys():
        print(f"Packing header to port {port}\n")
        message = sender + '\0' + receiver + ' ' + actual_message
        header = struct.pack('>bbhh', 4,0, len(message), len(sender + '\0' + receiver)) # Packing to the server the header of the request to send a message
        print(f"Sending broadcast header to port {port}\n")
        servers_im_connected_to[port].send(header) # Sending to the server the header of the request to send a message
        print(f"Sent broadcast header to port {port}\n")
        servers_im_connected_to[port].send(message.encode())
        print(f"Sent message to port {port}, waiting to see if {receiver} is connected to {port}....\n")
                                            
def handle_new_connection_from_client(conn_socket, length):
    recieved_client_name = conn_socket.recv(length).decode()
    if recieved_client_name not in connected_clients.keys():
        connected_clients[recieved_client_name] = conn_socket # adding the client and the connection to the client dictionary
        print(f"Successfully added {recieved_client_name} to my dictionary\n")
        print("My connected clients are: ", list(connected_clients.keys()), '\n')
        conn_socket.send(struct.pack('>bbhh', 2, 0, 0, 0))
        print("Sent to the client that i added his name to my dictionary\n")
    else:
        conn_socket.send(struct.pack('>bbhh', 30, 0, 0, 0)) # throw the message
        print(f"{recieved_client_name} is already in my dictionary\n")
        
def handle_messages(conn_socket, length, sublen):
    print("Recieved message header from client\n")
    receiver = conn_socket.recv(sublen).decode() # extracting the name of the destination client
    actual_message = conn_socket.recv(length-sublen).decode()[1:] # extracting the actual message without spacebar
    if receiver in connected_clients.keys(): # If the destination client is in my dictionary
        forward_message_between_clients_in_the_same_server(receiver, actual_message, conn_socket) 
    else: # If the destination client is not in my dictionary
        broadcast_message(receiver, actual_message, conn_socket)
    

def respond_to_client(conn_socket, client_address):
    while True:
        # print('start listening from', client_address, '\n')
        header = conn_socket.recv(6)
        type, subtype, length, sublen = struct.unpack('>bbhh', header)
        if type == 0 and subtype == 0: # the other server requested my clique
            handle_clique_request(conn_socket, client_address)
            
        elif type == 2 and subtype == 0: # A server connected to me through Clique, Therefore i need to update my clique
            port_to_add = conn_socket.recv(4) # the port i need to add to my dict
            sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            sock3.connect(('127.0.0.1', int(port_to_add.decode())))
            print("The new socket is: ", sock3, '\n')
            print("The address is: ", sock3.getsockname(), '\n')
            servers_im_connected_to[int(port_to_add.decode())] = sock3 # add the port that connects to me to my dict
            
        elif type == 2 and subtype == 1: # recieved new connection header from client
            handle_new_connection_from_client(conn_socket, length)
            
        elif type == 3 and subtype == 0: # recieved message header from client  
            handle_messages(conn_socket, length, sublen)
            
        elif type == 4 and subtype == 0: # recieved broadcast message header from server  
            sender, reciever = conn_socket.recv(sublen).decode().split('\0') # Unpacking the sender and reciever names
            message = conn_socket.recv(length-sublen).decode() # Unpacking the actual message
            print(f"Sender is {sender} sending a message to {reciever}\n")
            print("The message is: ", message, '\n')
            found_client = False
            for client in connected_clients.keys():
                if client == reciever:
                    found_client = True
                    connected_clients[client].send(struct.pack('>bbhh', 3, 0, len(sender +'\0' + reciever + ' ' + message), len(str(sender + '\0' + reciever))))
                    connected_clients[client].send((sender + '\0' + reciever).encode()) 
                    connected_clients[client].send(message.encode())
                    print(f"Sent message to {client}\n")
            if not found_client:
                print(f"{reciever} is not connected to this server, throwing the message\n")
                
        elif type == 5 and subtype == 0:
            print("Recieved from client request for my connected servers. Sending.......\n")
            my_connected_ports = repr(list(servers_im_connected_to.keys()))
            header = struct.pack('>bbhh', 5, 1, len(my_connected_ports),0)
            conn_socket.send(header)
            conn_socket.send(my_connected_ports.encode())
            
        elif type == 6 and subtype == 0:
            print("Recieved echo message from client. Sending echo back.......\n")
            echo_answer = conn_socket.send(struct.pack('>bbhh', 6, 1, 0, 0))
                

if __name__ == "__main__":    
                    
    servers_im_connected_to = {}
    connected_clients = {}

    ports_list = [4000, 4010, 4020, 4030, 4040]
    index_choice = int(input("Choose an index [0-4] : "))
    chosen_port = ports_list[index_choice]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.bind(('0.0.0.0', chosen_port))
    sock.listen(1)
    print("New server is listening on port number", chosen_port)  

    threading.Thread(target=try_connecting_to_other_servers).start()  
            
    while True:
        conn, client_address = sock.accept()
        print('new connection from', client_address)
        threading.Thread(target=respond_to_client, args=(conn, client_address)).start()
    
    

    
   