import socket
import struct
import threading
import time

def delete_connections_from_dict(connections_dict, delete_ports):
    for port in delete_ports:
        del(connections_dict[port]) 
    
    return connections_dict 
def calculate_minimal_port(minimal_socket):
    connections_dict = {}
    connections_dict[chosen_port_to_connect_to] = minimal_socket
    ports_to_check = ask_for_connected_ports(minimal_socket)
    ports_to_delete = []

    
    # Calculating first port rtt
    start = time.time()
    print(f"Sending echo to {chosen_port_to_connect_to} ...\n")
    echo_header = struct.pack('>bbhh', 6, 0, 0, 0) 
    minimal_socket.send(echo_header) # Sending to the server the echo message
    echo_response = minimal_socket.recv(6) # Recieving the echo message from the server
    type, subtype, length, sublen = struct.unpack('>bbhh', echo_response)
    if type == 6 and subtype == 1:
        done = time.time()
        minimal_rtt = done - start
        minimal_port = chosen_port_to_connect_to
        print(f"Recieved echo from {chosen_port_to_connect_to} with RTT of {minimal_rtt}\n")
    
    else:
        print(f"Echo didn't come from {chosen_port_to_connect_to}\n")
    
    for port in ports_to_check:
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        new_socket.connect(('127.0.0.1', port))
        connections_dict[port] = new_socket
        new_start = time.time()
        print(f"Sending echo to {port} ...\n")
        echo_header = struct.pack('>bbhh', 6, 0, 0, 0) 
        new_socket.send(echo_header) # Sending to the server the echo message
        echo_response = new_socket.recv(6) # Recieving the echo message from the server
        type, subtype, length, sublen = struct.unpack('>bbhh', echo_response)
        if type == 6 and subtype == 1:
            new_done = time.time()
            diffrence = new_done - new_start
            print(f"Recieved echo from {port} with RTT of {diffrence}\n")
            if diffrence < minimal_rtt:
                minimal_rtt = diffrence
                minimal_port = port
                
                
    for port in connections_dict.keys():
        if port != minimal_port:
            connections_dict[port].send(struct.pack('>bbhh', 7, 0, 0, 0)) # Send to the server to close the connection
            answer = connections_dict[port].recv(6)
            type, subtype, length, sublen = struct.unpack('>bbhh', answer)
            if type == 7 and subtype == 1:
                connections_dict[port].close()
                ports_to_delete.append(port)
                print(f"Closed connection to {port}\n")
            else:
                print(f"Error. Didn't close connection to {port}\n")
                
    
    connections_dict = delete_connections_from_dict(connections_dict, ports_to_delete) # Deleting the ports that are not the minimal port
                          
    print(f"The minimal port is {minimal_port} with a RTT of {minimal_rtt}")
    
    minimal_socket = connections_dict[minimal_port] # Saving the minimal RTT socket
    
    return minimal_port
        

def ask_for_connected_ports(minimal_socket):
    print(f"Asking for connected ports from {chosen_port_to_connect_to}...\n")
    header = struct.pack('>bbhh', 5, 0, 0, 0) # Header for the server to ask for connected ports
    minimal_socket.send(header) # Sending to the server the header of the request to ask for connected ports
    answer_header = minimal_socket.recv(6)
    type, subtype, length, sublen = struct.unpack('>bbhh', answer_header)
    if type == 5 and subtype == 1: # Server sent me the list of connected ports
        print(f"Recieved list of connected ports from {chosen_port_to_connect_to}. Unpacking...\n")
        ports_to_echo = eval(minimal_socket.recv(length).decode())
        print(f"The list of connected ports is: {ports_to_echo}\n")
            
    else:
        print(f"{chosen_port_to_connect_to} didn't send me the list of ports.\n")
    
    return ports_to_echo
            

def connect_client_to_server(minimal_socket):
    try:
        minimal_socket.connect(('127.0.0.1', chosen_port_to_connect_to))
        print(f"Connection to port {chosen_port_to_connect_to} successful.\n")
        minimal_port = calculate_minimal_port(minimal_socket)
        minimal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        minimal_socket.connect(('127.0.0.1', minimal_port))
        print(f"Connection to port {minimal_port} successful.\n")
        
        client_name = input('Enter your name: ')
        request_to_connect_header = struct.pack('>bbhh', 2,1,len(client_name),0) # Packing to the server the header of the request to connect
        print('Header of the client name packed.\n')
        minimal_socket.send(request_to_connect_header) # Sending to the server the header of the request to connect.
        minimal_socket.send(client_name.encode()) # Sending to the server the name of the client
        print('Header of the client name sent. Waiting for response from server...\n')
        
        answer_data = minimal_socket.recv(6)
        type, subtype, length, sublen = struct.unpack('>bbhh', answer_data)  # Receiving from the server the header of the response to the request to connect
        if type == 2 and subtype == 0: # Server added my name to it's dictionary
            print(f"{minimal_port} added my name to it's dictionary.\n")
        else:
            print(f"{minimal_port} didn't add my name.\n")
            exit()
            
    except Exception as e:
        print(f"Failed to connect to port.\n")
        print(e)
        exit()
        
    return minimal_socket
    
        
    


def wait_for_messages(minimal_socket):
    while True:
        recieved_message_header = minimal_socket.recv(6)
        type, subtype, length, sublen = struct.unpack('>bbhh', recieved_message_header)
        if type == 3: # recieved message header from client
            sender, reciever = minimal_socket.recv(sublen).decode().split('\0') # Unpacking the sender and reciever names
            message = minimal_socket.recv(length-sublen).decode()[1:] # Unpacking the actual message without the spacebar
            print(f"\nMessage from {sender} to {reciever}: {message}\n")
            



            
if __name__ == "__main__":       
    
             
    ports_list = [4000,4010,4020,4030,4040]
    index_port_to_connet_to = int(input('Enter index port to connect to [0-4]:'))
    chosen_port_to_connect_to = ports_list[index_port_to_connet_to]
    minimal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    
    minimal_socket = connect_client_to_server(minimal_socket)
    
    threading.Thread(target=wait_for_messages, args=(minimal_socket,)).start()

    while True:
        message = input("Enter your message in the format of: <client_name> <message> ")
        receiver = message.split(' ')[0]
        print("Receiver name:", receiver, '\n')
        message_header = struct.pack('>bbhh', 3, 0, len(message), len(receiver)) # Packing to the server the header of the request to send a message
        print("Request to send a message packed.\n")
        minimal_socket.send(message_header)# Sending to the server the header of the request to send a message
        minimal_socket.send(message.encode()) # Sending to the server the actual message
        print("Message sent.\n") 
    
