import pickle
import threading
import time

from ServerSocket import *
from ClientCollector import *
from Task import *

class Handler(threading.Thread):

    clientCollector = ClientCollector()

    def __init__(self, soc, addr, **kwargs):
        threading.Thread.__init__(self)
        self.soc = soc
        self.addr = addr
        self.exit = False

    def notifiyAll(self):
        for soc in self.clientCollector.getSocketList():
            task_update_client = Task("Remove Client", self.soc.getpeername()[1])
            obj = pickle.dumps(task_update_client)
            soc.send(obj)

    def run(self):
        try:
            while not self.exit:
                task = pickle.loads(self.soc.recv(4096))

                if task.getName() == "Submit ClientInfo":
                    clientInfo = task.getData()

                    if clientInfo.getAddress() not in self.clientCollector.getAddrList():
                        self.clientCollector.addClientInfo(clientInfo)

                    ### Add a new contact
                    for soc in self.clientCollector.getSocketList():
                        task_update_client = Task("New Client", self.clientCollector.getClientInfoList())
                        obj = pickle.dumps(task_update_client)
                        soc.send(obj)

                if task.getName() == "Message":
                    msgObject = task.getData()
                    receiverAddrList = msgObject.getReceiverAddr()

                    for soc in self.clientCollector.getSocketList():
                        for addr in receiverAddrList:
                            if self.soc != soc and soc.getpeername() == addr:
                                messageTask = Task("Message", msgObject)
                                obj = pickle.dumps(messageTask)
                                soc.send(obj)

        except ConnectionResetError:
            print(self.addr, " has been disconnected")
            self.exit = True
            self.clientCollector.removeSocket(self.soc)
            self.clientCollector.removeClientInfoByAddr(self.soc.getpeername())
            self.notifiyAll()
            self.soc.close()
















