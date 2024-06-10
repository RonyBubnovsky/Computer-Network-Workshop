import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.bind(('0.0.0.0', 9999))
sock.listen(1)

def respond_to_client(conn_socket, client_address):
    print('start listening from', client_address)
    while True:
        data = conn_socket.recv(1024)
        print('recieved from', client_address, 'text', data.decode())
        conn_socket.send(b'Echo: ' + data)
while True:
    conn, client_address = sock.accept()
    print('new connection from', client_address)
    threading.Thread(target=respond_to_client, args=(conn, client_address)).start()