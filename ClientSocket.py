import threading
import socket
import time
import pickle

from Task import *
from ClientInformation import *

class ClientSocket(threading.Thread):
    def __init__(self, ip, port, name="Name", **kwargs):
        threading.Thread.__init__(self)
        self.shutdown = False
        self.pauseMsg = True

        self.clientName = name
        self.clientMessage = ""

        self.ip = ip
        self.port = port
        self.targetServer = (ip, port)

        self.dataIncome = None

    def connect(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect(self.targetServer)
        self.soc.setblocking(1)

        self.recvThread = threading.Thread(target=self.receving)  ## Receiving Thread
        self.recvThread.start()

    def getAddr(self):
        return self.soc.getsockname()

    def getDataIncome(self):
        return self.dataIncome

    def receving(self):
        while not self.shutdown:
            try:
                data, addr = self.soc.recvfrom(4096)
                self.dataIncome = pickle.loads(data)
                print("Data from Handler:")
                for i in self.dataIncome:
                    print(i)

            except Exception as e:
                print(e)
                print("Error")
            finally:
                pass



    def setText(self, message):
        self.clientMessage = message

    def startMessaging(self):
        self.pauseMsg = False

    def pauseMessaging(self):
        self.pauseMsg = True

    def sendClientInformation(self, clientInfo):
        obj = pickle.dumps(clientInfo)
        self.soc.sendto(obj, self.targetServer)

    def sendMessage(self):
        if not self.pauseMsg:
            if self.clientMessage != "":
                string = self.clientName + ": " + self.clientMessage
                self.soc.sendto(string.encode("utf-8"), self.targetServer)

    def run(self):
        while True:
            self.sendMessage() ## Turn on sending messages function
            self.clientMessage = ""
            time.sleep(0.2)

    def close(self):
        self.shutdown = True
        self.recvThread.join()
        self.soc.close()


