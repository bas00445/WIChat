class Invitation:
    def __init__(self, receivedAddrs, ownerInfo, groupName):
        self.receivedAddrs = receivedAddrs
        self.ownerInfo = ownerInfo
        self.groupName = groupName

    def getReceiverAddr(self):
        return self.receivedAddrs

    def getOwnerInfo(self):
        return self.ownerInfo

    def getGroupName(self):
        return self.groupName
