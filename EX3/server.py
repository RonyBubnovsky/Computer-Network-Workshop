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

def ask_for_clique(connect_sock, port_to_add_to_dict):
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
        print("The clique Ports:", only_ports, '\n')
        
        return only_ports
    
        
def connect_to_servers_in_the_clique(clique_ports, my_port):
    count_connections = 0
    for port in clique_ports:
        if port != my_port:
            connect_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            connect_sock.connect(('127.0.0.1', port))
            print(f"{chosen_port} connected to {port} successfully Through Clique\n")
            count_connections += 1
            connect_sock.send(struct.pack('>bbhh', -30, -30, 0, 0))
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
                servers_im_connected_to[port] = connect_sock.getsockname() 
                clique_ports = ask_for_clique(connect_sock, chosen_port) # Ask for the clique of the other server
                connect_to_servers_in_the_clique(clique_ports, chosen_port) # Connect to the other servers in the received clique
                found_listening_server = True
            except ConnectionRefusedError:
                print(f"No server is listening on port {port}")
            

threading.Thread(target=try_connecting_to_other_servers).start()
def respond_to_client(conn_socket, client_address):
    print('start listening from', client_address)
    data = conn_socket.recv(6)
    type, subtype, length, sublen = struct.unpack('>bbhh', data)
    if type == 0 and subtype == 0: # the other server requested my clique
        print("request to send clique unpacked\n")
        port_to_add = conn_socket.recv(4) # the port i need to add to my dict
        servers_im_connected_to[int((port_to_add.decode()))] = client_address # add the port that connects to me to my dict
        print("The dict i need to send is: ", servers_im_connected_to, '\n')
        ip_and_ports_string = ""
        if len(servers_im_connected_to) > 0:
            for port, address in servers_im_connected_to.items():
                ip_and_ports_string += str(address[0]) + ':' + str(port) + '\0'
            data_to_unpack = struct.pack('>bbhh', 1, 0, len(ip_and_ports_string)-1, 0)
            print("clique to send packed\n")
            conn_socket.send(data_to_unpack)
            conn_socket.send(ip_and_ports_string[:-1].encode())
            print("clique to send sent\n")

while True:
    conn, client_address = sock.accept()
    print('new connection from', client_address, conn)
    threading.Thread(target=respond_to_client, args=(conn, client_address)).start()
    
   
