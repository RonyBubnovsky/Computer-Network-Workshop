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

def connect_to_clique(connect_sock):
    data = struct.pack('>bbhh', 0, 0, 0, 0)
    print("data packed\n")
    connect_sock.send(data)
    print("data sent\n")
    returned_data = connect_sock.recv(6)
    print("received first 6 bytes\n")
    type, subtype, length, sublen = struct.unpack('>bbhh', returned_data)
    unpacked_data = connect_sock.recv(length)
    print("received second bytes\n")
    print("wow:", unpacked_data.decode())

def try_connecting_to_other_servers():
    done_connecting = False
    for port in ports_list:
        if port != chosen_port and not done_connecting:
            try:
                connect_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                connect_sock.connect(('127.0.0.1', port))
                print(f"{chosen_port} connected to {port} successfully. {port} is sending its connected servers list to {chosen_port}...\n")
                servers_im_connected_to[port] = connect_sock.getsockname()
                print(f'{servers_im_connected_to}\n')
                connect_to_clique(connect_sock)
                done_connecting = True
            except ConnectionRefusedError:
                print(f"No server is listening on port {port}")

threading.Thread(target=try_connecting_to_other_servers).start()

def respond_to_client(conn_socket, client_address):
    print('start listening from', client_address)
    print("The dict i need to send is: ", servers_im_connected_to)
    data = conn_socket.recv(6)
    type, subtype, length, sublen = struct.unpack('>bbhh', data)
    print("data unpacked\n")
    if type == 0 and subtype == 0:
        ip_and_ports_string = ""
        if len(servers_im_connected_to) > 0:
            for port, address in servers_im_connected_to.items():
                ip_and_ports_string += str(port) + ':' + str(address[0]) + '\0'
            data_to_unpack = struct.pack('>bbhh', 1, 0, len(ip_and_ports_string), 0)
            conn_socket.send(data_to_unpack)
            conn_socket.send(ip_and_ports_string.encode())

while True:
    conn, client_address = sock.accept()
    print('new connection from', client_address)
    threading.Thread(target=respond_to_client, args=(conn, client_address)).start()
    
   
