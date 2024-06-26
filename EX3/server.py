import socket
import struct
import threading

servers_im_connected_to = {}
connected_clients = {}
servers_i_need_to_connect_to = ''

ports_list = [4000,4010,4020,4030,4040]
index_choice = int(input("Choose an index [0-4] :"))
chosen_port = ports_list[index_choice]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', chosen_port))
sock.listen(1)
print("New server is listening on port number",chosen_port)
        
      
def try_connecting_to_other_servers():
    done_connecting = False
    for port in ports_list:
        if port != chosen_port and done_connecting == False:
            try:
                connect_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                connect_sock.connect(('127.0.0.1', port))
                print(f"{chosen_port} connected to {port} successfully. {port} is sending it's connected servers list to {chosen_port}...")
                servers_im_connected_to[port] = connect_sock.getsockname()
                data = struct.pack('>bbhh', 0, 0, 0, 0)
                connect_sock.send(data)
                returned_data = connect_sock.recv(6)
                type, subtype, len, sublen = struct.unpack('>bbhh', returned_data)
                done_connecting = True
            except ConnectionRefusedError:
                print(f"No server is listening on port {port}")
                
             
threading.Thread(target=try_connecting_to_other_servers).start()



 
            
        
def respond_to_client(conn_socket, client_address):
    print('start listening from', client_address)
    data = conn_socket.recv(6)
    type, subtype, len, sublen = struct.unpack('>bbhh', data)
    if type == 0 and subtype == 0:
        pass
        
            
        
while True:
    conn, client_address = sock.accept()
    print('new connection from', client_address)
    threading.Thread(target=respond_to_client, args=(conn, client_address)).start()


    

    
    

    
