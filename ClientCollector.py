
class ClientCollector:
    def __init__(self):
        self.socketList = []
        self.addressList = []
        self.groupIDList = []
        self.handlerList = []

    def addSocket(self, client):
        self.socketList.append(client)
        print("All Clients: ", self.getAddressList())

    def addAddress(self, clientAddr):
        self.addressList.append(clientAddr)

    def addGroupIDList(self, groupID):
        self.groupIDList.append(groupID)

    def addHandler(self, clientHandler):
        self.handlerList.append(clientHandler)

    def getSocketList(self):
        return self.socketList

    def getAddressList(self):
        return self.addressList

    def getGroupIDList(self):
        return self.groupIDList

    def getHandlerList(self):
        return self.handlerList
