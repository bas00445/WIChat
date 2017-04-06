import pickle
import threading
import time



### เป็น server ย่อยๆ กระจายมาจาก server ###
class Handler(threading.Thread):
    def __init__(self, clientSocket, addr, clientCollector, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        self.clientSocket = clientSocket
        self.clientCollector = clientCollector
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











