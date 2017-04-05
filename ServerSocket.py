<<<<<<< HEAD
import threading
import socket
import time

from Handle import *

class ServerSocket:
    def __init__(self, ip, port, maximumClient = 10):
        self.ip = ip
        self.port = port
        self.server = ((ip, port))
        self.maximumClient = maximumClient

        self.clientSocketList = []
        self.clientAddrList = []
        self.groupIDList = []
        self.handlerList = []

    def start(self):
        try:
            self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socketServer.bind(self.server)
            self.socketServer.listen(self.maximumClient)
            self.socketServer.setblocking(1)
            print("Server is ready for connection.")
            self.listen()
        except OSError:
            print("Server Down.")

    def listen(self):
        try:
            while True:
                clientSocket, addr = self.socketServer.accept()

                ### Add an new address of the client
                if clientSocket not in self.clientAddrList:
                    self.clientAddrList.append(addr)
                    self.clientSocketList.append(clientSocket)
                    print("Append a new connection:", str(addr))

                handler = Handle(clientSocket, addr, self.clientSocketList)
                handler.start()

                self.handlerList.append(handler)

                for eachHandler in self.handlerList:
                    eachHandler.updateAllClients(self.clientAddrList)


        except OSError:
            print("Server Down.")


=======
import threading
import socket
import time

class ServerSocket:
    def __init__(self, ip, port, maximumClient = 10):
        self.ip = ip
        self.port = port
        self.server = ((ip, port))
        self.maximumClient = maximumClient

        self.clientList = []
        self.groupIDList = []

    def start(self):
        self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketServer.bind(self.server)
        self.socketServer.listen(self.maximumClient)
        self.socketServer.setblocking(1)
        print("Server is ready for connection.")
        self.listen()

    def listen(self):

        while True:
            clientSocket, addr = self.socketServer.accept()
            data = clientSocket.recv(1024).decode("ascii")
            ### Add an new address of the client
            if clientSocket not in self.clientList:
                self.clientList.append(addr)
                print("A new connection:", str(addr))

            if str(data) != "":
                print(time.ctime(time.time()) + str(addr) + ": :" + str(data))

            for client in self.clientList:
                self.socketServer.sendto("Response".encode("ascii"), client)


    def message1to1(self, start, goal, message):
        pass

    def message1toMany(self, start, goal, message):
        pass

>>>>>>> origin/master
ServerSocket("127.0.0.1", 5000).start()