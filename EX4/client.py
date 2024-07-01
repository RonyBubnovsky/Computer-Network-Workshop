import socket
import struct
import threading
import time


def calculate_minimal_port(socket):
    ports_to_check = ask_for_connected_ports(socket)
    print(f"Recieved list of connected ports from {chosen_port_to_connect_to} : {ports_to_check}\n")
    start = time.time()
    print(f"Sending echo to {chosen_port_to_connect_to} ...\n")
    echo_header = struct.pack('>bbhh', 6, 0, 0, 0) 
    socket.send(echo_header) # Sending to the server the header of the request to send an echo message
    socket.recv(6)
    done = time.time()
    minimal_rtt = done - start
    minimal_port = chosen_port_to_connect_to
    print(f"Recieved echo from {chosen_port_to_connect_to} with RTT of {minimal_rtt}\n")
    # for port in ports_to_check:
    #     start = time.time()
    #     done = time.time()
    #     diffrence = done - start
    #     if diffrence < minimal_rtt:
    #         minimal_rtt = diffrence
    #         minimal_port = port
            
    print(f"The minimal port is {minimal_port} with a RTT of {minimal_rtt}")
    
    return minimal_port
        

def ask_for_connected_ports(socket):
    print(f"Asking for connected ports from {chosen_port_to_connect_to}...\n")
    header = struct.pack('>bbhh', 5, 0, 0, 0) # Header for the server to ask for connected ports
    socket.send(header) # Sending to the server the header of the request to ask for connected ports
    answer_header = socket.recv(6)
    type, subtype, length, sublen = struct.unpack('>bbhh', answer_header)
    if type == 5 and subtype == 1: # Server sent me the list of connected ports
        print(f"Recieved list of connected ports from {chosen_port_to_connect_to}. Unpacking...\n")
        ports_to_echo = eval(socket.recv(length).decode())
        print(f"The list of connected ports is: {ports_to_echo}\n")
            
    else:
        print(f"{chosen_port_to_connect_to} didn't send me the list of ports.\n")
            

def connect_client_to_server(socket):
    try:
        socket.connect(('127.0.0.1', chosen_port_to_connect_to))
        print(f"Connection to port {chosen_port_to_connect_to} successful.\n")
        minimal_port = calculate_minimal_port(socket)
        
        
        client_name = input('Enter your name: ')
        request_to_connect_header = struct.pack('>bbhh', 2,1,len(client_name),0) # Packing to the server the header of the request to connect
        print('Header of the client name packed.\n')
        socket.send(request_to_connect_header) # Sending to the server the header of the request to connect.
        socket.send(client_name.encode()) # Sending to the server the name of the client
        print('Header of the client name sent. Waiting for response from server...\n')
        answer_data = socket.recv(6)
        type, subtype, length, sublen = struct.unpack('>bbhh', answer_data)  # Receiving from the server the header of the response to the request to connect
        if type == 2 and subtype == 0: # Server added my name to it's dictionary
            print(f"{chosen_port_to_connect_to} added my name to it's dictionary.\n")
        else:
            print(f"{chosen_port_to_connect_to} didn't add my name.\n")
            exit()
    except Exception as e:
        print(f"Failed to connect to port {chosen_port_to_connect_to}.\n")
        exit()
    


def wait_for_messages(socket):
    while True:
        recieved_message_header = socket.recv(6)
        type, subtype, length, sublen = struct.unpack('>bbhh', recieved_message_header)
        if type == 3: # recieved message header from client
            sender, reciever = socket.recv(sublen).decode().split('\0') # Unpacking the sender and reciever names
            message = socket.recv(length-sublen).decode()[1:] # Unpacking the actual message without the spacebar
            print(f"\nMessage from {sender} to {reciever}: {message}\n")
            



            
if __name__ == "__main__":       
    
             
    ports_list = [4000,4010,4020,4030,4040]
    index_port_to_connet_to = int(input('Enter index port to connect to [0-4]:'))
    chosen_port_to_connect_to = ports_list[index_port_to_connet_to]
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    minimal_port = chosen_port_to_connect_to
    minimal_rtt = None

    connect_client_to_server(socket)
    

    threading.Thread(target=wait_for_messages, args=(socket,)).start()

    while True:
        message = input("Enter your message in the format of: <client_name> <message> ")
        receiver = message.split(' ')[0]
        print("Receiver name:", receiver, '\n')
        message_header = struct.pack('>bbhh', 3, 0, len(message), len(receiver)) # Packing to the server the header of the request to send a message
        print("Request to send a message packed.\n")
        socket.send(message_header)# Sending to the server the header of the request to send a message
        socket.send(message.encode()) # Sending to the server the actual message
        print("Message sent.\n") 
    
