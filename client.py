<<<<<<< HEAD
import socket
import threading
import time
import pickle

tLock = threading.Lock()
shutdown = False

def receving(name, sock):
    while not shutdown:
        tLock.acquire()
        try:
            data, addr = sock.recvfrom(1024)
            if data != "":
                print(data)

        except:
            pass
        finally:
            tLock.release()

host = "127.0.0.1"
port = 5000

server = (host,5000)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.setblocking(0)


rT = threading.Thread(target=receving, args=("RecvThread",s)) ## Receiving Thread
rT.start()
alias = input("Name: ")
message = input(alias + "->")

while message != "q":
    string = alias + ": " + message
    if message != "":
        s.sendto(string.encode("ascii"), server)
    tLock.acquire()
    message = input(alias + "->")
    tLock.release()
    time.sleep(0.2)

shutdown = True
rT.join()
s.close()
=======
import socket
import threading
import time

tLock = threading.Lock()
shutdown = False

def receving(name, sock):
    while not shutdown:
        tLock.acquire()
        try:
            data, addr = sock.recvfrom(1024)
            print(data)

        except:
            pass
        finally:
            tLock.release()

host = "127.0.0.1"
port = 5000

server = (host,5000)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.setblocking(0)


rT = threading.Thread(target=receving, args=("RecvThread",s)) ## Receiving Thread
rT.start()
alias = input("Name: ")
message = input(alias + "->")

while message != "q":
    string = alias + ": " + message
    if message != "":
        s.sendto(string.encode("ascii"), server)
    tLock.acquire()
    message = input(alias + "->")
    tLock.release()
    time.sleep(0.2)

shutdown = True
rT.join()
s.close()
>>>>>>> origin/master
