import pickle
import threading
import time

from ServerSocket import *

### เป็น server ย่อยๆ กระจายมาจาก server ###
class Handler(threading.Thread):
    def __init__(self, clientSocket, addr, **kwargs):
        threading.Thread.__init__(self)

        self.clientSocket = clientSocket
        self.addr = addr
        self.exit = False

    def run(self):
        try:
            while not self.exit:
                data = self.clientSocket.recv(1024).decode("ascii")  ## รับ data จาก client
                string = "Data from " + str(self.addr) + ":" + data
                self.clientSocket.send(string.encode("ascii"))

        except ConnectionResetError:
            print(self.addr, " has been disconnected")











