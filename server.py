import socket
import time

host = "192.168.43.128"
port = 5000

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

quitting = False

print("Server Started.")

while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        if "Quit" in str(data):
            qutting = True

        if addr not in clients:
            clients.append(addr)

        print(time.ctime(time.time()) + str(addr) + ": :" + str(data))

        for client in clients:
            s.sendto(data.decode("utf-8"), client)

    except:
        pass

s.close()

