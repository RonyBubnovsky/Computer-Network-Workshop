import socket
import struct

ports_list = [4000,4010,4020,4030,4040]
index_port_to_connet_to = int(input('Enter index port to connect to [0-4]:'))
chosen_port_to_connet_to = ports_list[index_port_to_connet_to]
def connect_client_to_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.connect(('127.0.0.1', chosen_port_to_connet_to))
    print(f"Connection to port {chosen_port_to_connet_to} successful.\n")

    client_name = input('Enter your name:')
    request_to_connect_header = struct.pack('>bbhh', 2,1,len(client_name),0) # Packing to the server the header of the request to connect
    print('Header of the client name packed.\n')
    sock.send(request_to_connect_header) # Sending to the server the header of the request to connect
    clinet_name_data = sock.send(client_name.encode()) # Sending to the server the name of the client
    print('Header of the client name sent. Waiting for response from server...\n')
    answer_data = sock.recv(6)
    type, subtype, length, sublen = struct.unpack('>bbhh', answer_data)  # Receiving from the server the header of the response to the request to connect
    if type == 2 and subtype == 0:
        print(f"{chosen_port_to_connet_to} added my name to it's dictionary.\n")
    else:
        print(f"{chosen_port_to_connet_to} didn't add my name.\n")
    
connect_client_to_server()
while True:
    # data = input('Enter line:').strip().encode()
    # sock.send(data)
    # reply_data = sock.recv(1024)
    # print('server reply:', reply_data.decode())
    pass
