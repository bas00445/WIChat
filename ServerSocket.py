import threading
import socket
import time

from Handler import *
from ClientCollector import ClientCollector


class ServerSocket(threading.Thread):
    def __init__(self, ip, port, maximumClient = 10, **kwargs):
        threading.Thread.__init__(self)

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
        except OSError as e:
            print("Server Down: ", e)

    def listen(self):
        try:
            while True:
                clientSocket, addr = self.socketServer.accept()

                handler = Handler(clientSocket, addr, self.clientCollector)
                handler.start()
                handler.clientCollector.addSocket(clientSocket)
                handler.clientCollector.addHandler(handler)

                time.sleep(0.5) ## Wait a bit for updating value in a Handler object

        except OSError as e:
            print("Server Down: ", e)

