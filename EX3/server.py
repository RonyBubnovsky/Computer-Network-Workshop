import socket
import struct
import threading

servers_im_connected_to = {}
connected_clients = {}

ports_list = [4000, 4010, 4020, 4030, 4040]
index_choice = int(input("Choose an index [0-4] :"))
chosen_port = ports_list[index_choice]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', chosen_port))
sock.listen(1)
print("New server is listening on port number", chosen_port)

def ask_for_clique(connect_sock, port_to_add_to_dict, port):
    data = struct.pack('>bbhh', 0, 0, 0, 0)
    print("request to get the clique packed\n")
    
    connect_sock.send(data)
    connect_sock.send(str(port_to_add_to_dict).encode())
    print("request to get the clique sent\n")
    
    returned_data = connect_sock.recv(6)
    print("received first 6 bytes of clique answer\n")
    
    type, subtype, length, sublen = struct.unpack('>bbhh', returned_data)
    if type == 1 and subtype == 0: # Answer from the server. receiving the clique.
        unpacked_data = connect_sock.recv(length)
        print("received the clique data\n")
        print("the clique:", unpacked_data.decode(), '\n')
        
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
            connect_sock.send(struct.pack('>bbhh', 33, 0, 0, 0)) # Update the clique of the server i connected to
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
                clique_ports = ask_for_clique(connect_sock, chosen_port, port) # Ask for the clique of the other server
                connect_to_servers_in_the_clique(clique_ports, chosen_port) # Connect to the other servers in the received clique
                found_listening_server = True
            except ConnectionRefusedError:
                print(f"No server is listening on port {port}")
  
def handle_clique_request(conn_socket, client_address):
    print("request to send clique unpacked\n")
    port_to_add = conn_socket.recv(4) # the port i need to add to my dict
    servers_im_connected_to[int((port_to_add.decode()))] = conn_socket # add the port that connects to me to my dict
    print("The dict i need to send is: ", servers_im_connected_to, '\n')
    ip_and_ports_string = ""
    if len(servers_im_connected_to) > 0:
        for port in servers_im_connected_to.keys():
            ip_and_ports_string += '127.0.0.1' + ':' + str(port) + '\0'
        data_to_unpack = struct.pack('>bbhh', 1, 0, len(ip_and_ports_string)-1, 0)
        print("clique to send packed\n")
        conn_socket.send(data_to_unpack)
        conn_socket.send(ip_and_ports_string[:-1].encode())
        print("socket that is working" , conn_socket)
        print("clique to send sent\n")         

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
    print("My connected ports are: ", list(servers_im_connected_to.keys()), '\n')
    for client, socket in connected_clients.items():
        if socket == conn_socket: # Finding the source client
            sender = client 
    for port in servers_im_connected_to.keys():
        print("My ports are: ", list(servers_im_connected_to.keys()), '\n')
        print(f"Packing header to port {port}\n")
        print(f"my ports are: ", list(servers_im_connected_to.keys()), '\n')
        message = sender + '\0' + receiver + ' ' + actual_message
        header = struct.pack('>bbhh', 4,0, len(message), len(sender + '\0' + receiver)) # Packing to the server the header of the request to send a message
        print(f"Sending header to port {port}\n")
        servers_im_connected_to[port].send(header) # Sending to the server the header of the request to send a message
        print(f"Sent header to port {port}\n")
        servers_im_connected_to[port].send(message.encode())
        print(f"Sent message to port {port}\n")
        
        

                                    
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
    print("recieved message header from client\n")
    receiver = conn_socket.recv(sublen).decode() # extracting the name of the destination client
    actual_message = conn_socket.recv(length-sublen).decode()[1:] # extracting the actual message without spacebar
    if receiver in connected_clients.keys(): # If the destination client is in my dictionary
        forward_message_between_clients_in_the_same_server(receiver, actual_message, conn_socket) 
    else: # If the destination client is not in my dictionary
        broadcast_message(receiver, actual_message, conn_socket)
    
         
threading.Thread(target=try_connecting_to_other_servers).start()
def respond_to_client(conn_socket, client_address):
    while True:
        print('start listening from', client_address, '\n')
        header = conn_socket.recv(6)
        type, subtype, length, sublen = struct.unpack('>bbhh', header)
        if type == 0 and subtype == 0: # the other server requested my clique
            handle_clique_request(conn_socket, client_address)
            
        elif type == 33: # A server connected to me through Clique, Therefore i need to update my clique
            port_to_add = conn_socket.recv(4) # the port i need to add to my dict
            servers_im_connected_to[int((port_to_add.decode()))] = conn_socket # add the port that connects to me to my dict
            
        elif type == 2 and subtype == 1: # recieved new connection header from client
            handle_new_connection_from_client(conn_socket, length)
            
        elif type == 3 and subtype == 0: # recieved message header from client  
            handle_messages(conn_socket, length, sublen)
            
        elif type == 4 and subtype == 0: # recieved broadcast message header from server  
            print("im it type 4")
            sender, reciever = conn_socket.recv(sublen).decode().split('\0') # Unpacking the sender and reciever names
            message = conn_socket.recv(length-sublen).decode() # Unpacking the actual message
            print(f"sender is {sender} sending a message to {reciever}\n")
            print("The message is: ", message, '\n')
            for client in connected_clients.keys():
                if client == reciever:
                    connected_clients[client].send(struct.pack('>bbhh', 3, 0, len(sender +'\0' + reciever + ' ' + message), len(str(sender + '\0' + reciever))))
                    connected_clients[client].send((sender + '\0' + reciever).encode()) 
                    connected_clients[client].send(message.encode())
                    print(f"Sent message to {client}\n")
    
            
while True:
    conn, client_address = sock.accept()
    print('new connection from', client_address)
    threading.Thread(target=respond_to_client, args=(conn, client_address)).start()
    
   