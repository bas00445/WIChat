class FileObject:
    def __init__(self, bytesData, ownerID, receiverAddrList):
        self.bytesData = bytesData
        self.ownerID = ownerID
        self.receiverAddrList = receiverAddrList

    def getBytesData(self):
        return self.bytesData

    def getOwnerID(self):
        return self.ownerID

    def getReceiverAddr(self):
        return self.receiverAddrList
