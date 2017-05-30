import pickle
import threading
import time
import os

from ServerSocket import *
from ClientCollector import *
from Task import *
from FileObject import *

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

    def transferFile(self, soc, directory, fileObj):

        file = open(directory, "rb")
        task = Task("StoreFile", fileObj)
        obj = pickle.dumps(task)

        soc.send(obj)

        data = file.read(1024)
        while data:
            soc.send(data)
            data = file.read(1024)

        file.close()
        print("TransferFile: Close file.")

    def run(self):
        try:
            while not self.exit:
                try:
                    data = self.soc.recv(1024)

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
                        receiverAddrs = msgObject.getReceiverAddr()

                        for soc in self.clientCollector.getSocketList():
                            for addr in receiverAddrs:
                                if self.soc != soc and soc.getpeername()[1] == int(addr):
                                    obj = pickle.dumps(task)
                                    soc.send(obj)

                    if task.getName() == "Group Message":
                        msgObject = task.getData()
                        receiverAddrs = msgObject.getReceiverAddr()

                        for soc in self.clientCollector.getSocketList():
                            for addr in receiverAddrs:
                                if self.soc != soc and soc.getpeername()[1] == int(addr):
                                    obj = pickle.dumps(task)
                                    soc.send(obj)

                    if task.getName() == "Update Group Members":
                        groupChat = task.getData()
                        receiverAddrs = groupChat.getMemberIDList()

                        for soc in self.clientCollector.getSocketList():
                            for addr in receiverAddrs:
                                if self.soc != soc and soc.getpeername()[1] == int(addr):
                                    print("Update Group Members")
                                    obj = pickle.dumps(task)
                                    soc.send(obj)

                    if task.getName() == "Invite to group":
                        inviteObj = task.getData()
                        receiverAddrs = inviteObj.getReceiverAddr()
                        for soc in self.clientCollector.getSocketList():
                            for addr in receiverAddrs:
                                if self.soc != soc and soc.getpeername()[1] == int(addr):
                                    obj = pickle.dumps(task)
                                    soc.send(obj)

                    if task.getName() == "Response Invitation":
                        inviteObj = task.getData()
                        receiverAddrs = inviteObj.getReceiverAddr()
                        for soc in self.clientCollector.getSocketList():
                            for addr in receiverAddrs:
                                if self.soc != soc and soc.getpeername()[1] == int(addr):
                                    obj = pickle.dumps(task)
                                    soc.send(obj)

                    if task.getName() == "Change Status":
                        clientInfo = task.getData()
                        for soc in self.clientCollector.getSocketList():
                            task_update_client = Task("Change Status", clientInfo)
                            obj = pickle.dumps(task_update_client)
                            soc.send(obj)


                    if task.getName() == "Send File":
                        obj = task.getData()
                        receiverAddrs = obj.getReceiverAddr()
                        for soc in self.clientCollector.getSocketList():
                            for addr in receiverAddrs:
                                if self.soc != soc and soc.getpeername()[1] == addr[1]:
                                    filename = obj.getFilename()
                                    filesize = obj.getFileSize()
                                    directory = "download/" + filename
                                    file = open(directory, "wb")
                                    data = self.soc.recv(1024)
                                    targetSize = filesize
                                    currentSize = 0
                                    if filesize <= 1024:
                                        file.write(data)
                                    elif filesize > 1024:
                                        while filesize >= 0:
                                            print(">>Receiving a file : ", str(100*currentSize//targetSize) + " % <<")
                                            file.write(data)
                                            currentSize += 1024
                                            filesize -= 1024
                                            if filesize < 0:
                                                break
                                            data = self.soc.recv(1024)

                                    file.close()
                                    print("Server received a new file.")
                                    print("Closed file.")

                                    self.transferFile(soc, directory, obj)

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
















