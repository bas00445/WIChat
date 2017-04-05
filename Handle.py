import pickle
import threading
import time

class Handle(threading.Thread):
    def __init__(self, clientSocket, addr, allClients, **kwargs):
        threading.Thread.__init__(self)

        self.clientSocket = clientSocket
        self.addr = addr
        self.allClients = allClients
        self.exit = False


    def run(self):
        try:
            while not self.exit:
                data = self.clientSocket.recv(1024).decode("ascii")
                print("All Clients: ", self.allClients)
                string = "Data from " + str(self.addr) + ":" + data
                self.clientSocket.send(string.encode("ascii"))


        except ConnectionResetError:
            print(self.addr, " has been disconnected")


    def updateAllClients(self, new):
        self.allClients = new






