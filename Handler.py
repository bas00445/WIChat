import pickle
import threading
import time

from ServerSocket import *
from ClientCollector import *

### เป็น server ย่อยๆ กระจายมาจาก server ###
class Handler(threading.Thread):
    clientCollector = ClientCollector()

    def __init__(self, clientSocket, addr, clientCollector, **kwargs):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket

        self.addr = addr
        self.exit = False

    def run(self):

        try:
            while not self.exit:

                # รับ ClientInformation จาก client
                clientInfo = pickle.loads(self.clientSocket.recv(4096))
                if clientInfo.getAddress() not in self.clientCollector.getAddrList():
                    print(">>Append a new connection:", str(clientInfo) + "\n")
                    self.clientCollector.addClientInfo(clientInfo)

                for clientSocket in self.clientCollector.getSocketList():
                    clientSocket.send(pickle.dumps(self.clientCollector.getClientInfoList()))

        except ConnectionResetError:
            self.clientCollector.removeClientInfo(clientInfo)

            print(self.addr, " has been disconnected")












