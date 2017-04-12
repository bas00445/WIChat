import threading
import socket
import time
import pickle

from Task import *
from ClientInformation import *
from Message import *

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
                task = pickle.loads(self.soc.recv(4096))
                self.dataIncome = task

            except Exception as e:
                print(e)

            finally:
                pass

    def setText(self, message):
        self.clientMessage = message

    def startMessaging(self):
        self.pauseMsg = False

    def pauseMessaging(self):
        self.pauseMsg = True

    def sendTask(self, task):
        obj = pickle.dumps(task)
        self.soc.sendto(obj, self.targetServer)

    def setTargetAddress(self, newTargetAddr):
        self.targetServer = newTargetAddr

    def run(self):
        while True:
            if self.clientMessage != "":
                text = self.clientName + ": " + self.clientMessage
                msg = Message(text)
                task_send_message = Task("Message", msg)
                obj = pickle.dumps(task_send_message)

                self.soc.sendto(obj, self.targetServer)

            self.clientMessage = ""
            time.sleep(0.2)

    def close(self):
        self.shutdown = True
        self.recvThread.join()
        self.soc.close()


