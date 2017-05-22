import pickle
import threading
import time
import os

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
        self.tLock = threading.Lock()

    def notifiyAll(self):
        for soc in self.clientCollector.getSocketList():
            task_update_client = Task("Remove Client", self.soc.getpeername()[1])
            obj = pickle.dumps(task_update_client)
            soc.send(obj)

    def run(self):
        try:
            while not self.exit:
                try:
                    data = self.soc.recv(4096)
                    if not data:
                        continue

                    if data:
                        task = pickle.loads(data)

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
                            messageTask = Task("Message", msgObject)
                            obj = pickle.dumps(messageTask)
                            soc.send(obj)

                    if task.getName() == "Send File":
                        obj = task.getData()
                        receiverAddrList = obj.getReceiverAddr()
                        for soc in self.clientCollector.getSocketList():
                            for addr in receiverAddrList:
                                print("Send file: ", soc.getpeername(), addr)
                                if self.soc != soc and soc.getpeername()[1] == addr[1]:
                                    filename = obj.getFilename()
                                    filesize = obj.getFileSize()

                        file = open(filename, 'wb')

                        data = self.soc.recv(4096)
                        targetSize = filesize
                        currentSize = 0
                        if filesize <= 4096:
                            file.write(data)
                        elif filesize > 4096:
                            while filesize >= 0:
                                print(">>Receiving a file : ", str(100*currentSize//targetSize) + " % <<")
                                file.write(data)
                                currentSize += 4096
                                filesize -= 4096
                                if filesize <= 0:
                                    break
                                data = self.soc.recv(4096)

                        print("Transfer has been finished!!")
                        print("Closed file")
                        file.close()

                except OverflowError:
                    pass
                except ValueError:
                    pass
                except KeyError:
                    pass
                except EOFError:
                    pass
                except pickle.UnpicklingError:
                    pass
                except pickle.PicklingError:
                    pass
                except pickle.PickleError:
                    pass

        except ConnectionResetError:
            print(self.addr, " has been disconnected")
            self.exit = True
            self.clientCollector.removeSocket(self.soc)
            self.clientCollector.removeClientInfoByAddr(self.soc.getpeername())
            self.notifiyAll()
            self.soc.close()
















