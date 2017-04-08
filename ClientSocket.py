import threading
import socket
import time
import pickle

from Task import *
from ClientInformation import *

class ClientSocket(threading.Thread):
    def __init__(self, ip, port, name="Name", **kwargs):
        threading.Thread.__init__(self)
        self.tLock = threading.Lock()
        self.shutdown = False
        self.pauseMsg = True

        self.clientName = name
        self.clientMessage = ""

        self.ip = ip
        self.port = port
        self.targetServer = (ip, port)

    def connect(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect(self.targetServer)
        self.soc.setblocking(1)

        self.recvThread = threading.Thread(target=self.receving, args=("RecvThread", self.soc))  ## Receiving Thread
        self.recvThread.start()

    def getAddr(self):
        return self.soc.getsockname()

    def receving(self, name, sock):
        while not self.shutdown:
            self.tLock.acquire()
            try:
                data, addr = sock.recvfrom(1024)
                if data != "":
                    print(data)
            except:
                pass
            finally:
                self.tLock.release()

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


