import pickle
import threading
import time

from ServerSocket import *

from ClientInformation import *

global clientCollector

### เป็น server ย่อยๆ กระจายมาจาก server ###
class Handler(threading.Thread):
    def __init__(self, clientSocket, addr, clientCollector, **kwargs):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.addr = addr
        self.clientCollector = clientCollector
        self.exit = False

    def run(self):
        try:
            while not self.exit:

                # รับ ClientInformation จาก client
                clientInfo = pickle.loads(self.clientSocket.recv(4096))
                if clientInfo.getAddress() not in self.clientCollector.getAddrList():
                    print(">>Append a new connection:", str(clientInfo) + "\n")
                    self.clientCollector.addClientInfo(clientInfo)

                for clientAddr in self.clientCollector.getAddrList():
                    self.clientSocket.sendto(pickle.dumps(self.clientCollector.getClientInfoList()), clientAddr)

        except ConnectionResetError:
            self.clientCollector.removeClientInfo(clientInfo)
            print(self.addr, " has been disconnected")












