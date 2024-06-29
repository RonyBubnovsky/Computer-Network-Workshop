import socket
import struct
import threading

ports_list = [4000,4010,4020,4030,4040]
index_port_to_connet_to = int(input('Enter index port to connect to [0-4]:'))
chosen_port_to_connet_to = ports_list[index_port_to_connet_to]
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
def connect_client_to_server(socket):
    socket.connect(('127.0.0.1', chosen_port_to_connet_to))
    print(f"Connection to port {chosen_port_to_connet_to} successful.\n")

    client_name = input('Enter your name:')
    request_to_connect_header = struct.pack('>bbhh', 2,1,len(client_name),0) # Packing to the server the header of the request to connect
    print('Header of the client name packed.\n')
    socket.send(request_to_connect_header) # Sending to the server the header of the request to connect
    clinet_name_data = socket.send(client_name.encode()) # Sending to the server the name of the client
    print('Header of the client name sent. Waiting for response from server...\n')
    answer_data = socket.recv(6)
    type, subtype, length, sublen = struct.unpack('>bbhh', answer_data)  # Receiving from the server the header of the response to the request to connect
    if type == 2 and subtype == 0: # Server added my name to it's dictionary
        print(f"{chosen_port_to_connet_to} added my name to it's dictionary.\n")
    else:
        print(f"{chosen_port_to_connet_to} didn't add my name.\n")
    
connect_client_to_server(socket)

def wait_for_messages(socket):
    while True:
        recieved_message_header = socket.recv(6)
        type, subtype, length, sublen = struct.unpack('>bbhh', recieved_message_header)
        if type == 3: # recieved message header from client
            sender, reciever = socket.recv(sublen).decode().split('\0') # Unpacking the sender and reciever names
            message = socket.recv(length-sublen).decode()[1:] # Unpacking the actual message
            print(f"\nMessage from {sender} to {reciever}: {message}\n")

threading.Thread(target=wait_for_messages, args=(socket,)).start()

while True:
    message = input("Enter your message in the format of: <client_name> <message> ")
    destination_client_name = message.split(' ')[0]
    print("destination client name:", destination_client_name, '\n')
    if socket is not None:
        message_header = struct.pack('>bbhh', 3, 0, len(message), len(destination_client_name)) # Packing to the server the header of the request to send a message
        print("Request to send a message packed.\n")
        socket.send(message_header)# Sending to the server the header of the request to send a message
        socket.send(message.encode()) # Sending to the server the actual message
        print("Message sent.\n") 