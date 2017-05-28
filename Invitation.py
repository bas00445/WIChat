class Invitation:
    def __init__(self, receivedAddrs, ownerInfo, groupName, response = False):
        self.receivedAddrs = receivedAddrs
        self.ownerInfo = ownerInfo
        self.groupName = groupName
        self.response = response

    def getReceiverAddr(self):
        return self.receivedAddrs

    def getOwnerInfo(self):
        return self.ownerInfo

    def getGroupName(self):
        return self.groupName

    def getResponse(self):
        return self.response

