import socket

UDP_IP = '0.0.0.0'
UDP_PORT = 9999
opened_user = {"name_to_addr": {}, "addr_to_name": {}}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.bind((UDP_IP, UDP_PORT))

try:
    while True:
        data, addr = sock.recvfrom(1024)

        if addr not in opened_user["name_to_addr"].values() and len(data.decode().split()) != 1:
            sock.sendto("Invalid Client Name\nPlease enter a different name: ".encode(), addr)
        else:
            if addr not in opened_user["name_to_addr"].values() and data.decode().strip() not in opened_user["name_to_addr"].keys():
                username = data.decode().strip()
                opened_user["name_to_addr"][username] = addr
                opened_user["addr_to_name"][addr] = username
                print(f"New Client Registered To Server: {username} {addr}")

            elif addr not in opened_user["name_to_addr"].values() and data.decode().strip() in opened_user["name_to_addr"].keys():
                sock.sendto("Client Already Exists\nPlease enter a different name: ".encode(), addr)
                print("Tried to register an existing client.")

            else:
                dest_user, msg = data.decode().split(' ', 1)
                dest_user = dest_user.strip()
                if dest_user in opened_user["name_to_addr"].keys():
                    sock.sendto(msg.encode() + " from ".encode() + opened_user["addr_to_name"][addr].encode(),
                                opened_user["name_to_addr"][dest_user])
                else:
                    sock.sendto("There isn't such a user".encode(), addr)

finally:
    sock.close()

