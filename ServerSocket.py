import threading
import socket
import time

from Handler import *
from ClientCollector import ClientCollector

class ServerSocket(threading.Thread):
    def __init__(self, ip, port, maximumClient = 10, **kwargs):
        threading.Thread.__init__(self, **kwargs)

        self.ip = ip
        self.port = port
        self.server = ((ip, port))
        self.maximumClient = maximumClient
        self.clientCollector = ClientCollector()

    def run(self):
        self.startServer()

    def startServer(self):
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
                if clientSocket not in self.clientCollector.getSocketList():
                    self.clientCollector.addAddress(addr)
                    self.clientCollector.addSocket(clientSocket)
                    print("Append a new connection:", str(addr))

                handler = Handler(clientSocket, addr, self.clientCollector)
                handler.start()

                self.clientCollector.addHandler(handler)

        except OSError:
            print("Server Down.")

