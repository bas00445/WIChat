
class ClientCollector:
    def __init__(self, **kwargs):
        self.clientInfoList = []
        self.addressList = []
        self.groupChatList = []
        self.handlerList = []
        self.socketList = []


    def addSocket(self, clientSocket):
        self.socketList.append(clientSocket)

    def addClientInfo(self, clientInfo):
        self.clientInfoList.append(clientInfo)
        self.addressList.append(clientInfo.getAddress())

    def showAllClients(self):
        for eachClientInfo in self.clientInfoList:
            print(eachClientInfo)

    def addGroupChat(self, group):
        self.groupChatList.append(group)

    def addHandler(self, clientHandler):
        self.handlerList.append(clientHandler)

    def removeClientInfoByAddr(self, addr):
        for clientInfo in self.clientInfoList:
            if clientInfo.getAddress() == addr:
                self.clientInfoList.remove(clientInfo)

    def setNewStatus(self, id, status):
        for clientInfo in self.clientInfoList:
            if clientInfo.getID() == id:
                clientInfo.setStatus(status)

    def removeSocket(self, soc):
        self.socketList.remove(soc)

    def getClientInfoList(self):
        return self.clientInfoList

    def getClientNameList(self):
        lst = []
        for client in self.clientInfoList:
            lst.append(client.getName())

        return lst

    def getSocketList(self):
        return self.socketList


    def getAddrList(self):
        return self.addressList

    def getAllClientInfo(self):
        s = "\n"

        for client in self.clientInfoList:
            s += "\t" + str(client) + "\n"

        return s

