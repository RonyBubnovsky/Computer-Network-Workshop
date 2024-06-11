import socket
import threading

ports_list = [5000,5010,5020,5030,5041]
index_choice = int(input("Choose an index [0-4] :"))
chosen_port = ports_list[index_choice]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', chosen_port))
sock.listen(1)
print("New server is listening on port number",chosen_port)
        
      
def wait_for_accept():
    for port in ports_list:
        if port != chosen_port:
            try:
                connect_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                connect_sock.connect(('127.0.0.1', port))
                print(f"{chosen_port} connected to {port} successfully")
                connect_sock.send("Hello".encode())
                print(f"{port} Server reply:", connect_sock.recv(1024).decode())
                connect_sock.close()
            except ConnectionRefusedError:
                print(f"No server is listening on port {port}")
                
             
threading.Thread(target=wait_for_accept).start()
 
            
        
def respond_to_client(conn_socket, client_address):
    print('start listening from', client_address)
    data = conn_socket.recv(1024)
    print('recieved from', client_address, 'text', data.decode())
    conn_socket.send('World\nEnd'.encode())
            
        
while True:
    conn, client_address = sock.accept()
    print('new connection from', client_address)
    threading.Thread(target=respond_to_client, args=(conn, client_address)).start()
    

    