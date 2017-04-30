import pickle
import threading
import time

from ServerSocket import *
from ClientCollector import *
from Task import *

class Handler(threading.Thread):

    clientCollector = ClientCollector()

    def __init__(self, soc, addr, clientCollector, **kwargs):
        threading.Thread.__init__(self)
        self.soc = soc
        self.addr = addr
        self.exit = False

    def run(self):
        try:
            while not self.exit:

                task = pickle.loads(self.soc.recv(4096))

                if task.getName() == "Submit ClientInfo":
                    clientInfo = task.getData()

                    if clientInfo.getAddress() not in self.clientCollector.getAddrList():
                        self.clientCollector.addClientInfo(clientInfo)

                    ### Update contact list to all clients in the server
                    for soc in self.clientCollector.getSocketList():
                        task_update_client = Task("All ClientInfo", self.clientCollector.getClientInfoList())
                        obj = pickle.dumps(task_update_client)
                        soc.send(obj)

                if task.getName() == "Message":
                    msgObject = task.getData()
                    for soc in self.clientCollector.getSocketList():
                        receiverAddrList = msgObject.getReceiverAddr()

                        for addr in receiverAddrList:
                            if self.soc != soc and soc.getpeername() == addr:
                                messageTask = Task("Message", msgObject)
                                obj = pickle.dumps(messageTask)
                                soc.send(obj)


        except ConnectionResetError:
            self.exit = True
            self.soc.close()
            print(self.addr, " has been disconnected")











