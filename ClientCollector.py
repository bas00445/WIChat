
class ClientCollector:
    def __init__(self, **kwargs):
        self.clientInfoList = []
        self.addressList = []
        self.groupChatList = []
        self.handlerList = []

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

    def removeClientInfo(self, clientInfo):
        self.clientInfoList.remove(clientInfo)

    def getClientInfoList(self):
        return self.clientInfoList

    def getGroupChat(self):
        return self.groupChatList

    def getHandlerList(self):
        return self.handlerList

    def getAddrList(self):
        return self.addressList

    def getAllClientInfo(self):
        s = "All Client Informations:" + "\n"
        for client in self.clientInfoList:
            s += "\t" + str(client) + "\n"

        return s

