class FileObject:
    def __init__(self, filename, ownerID, receiverAddrList):
        self.filename = filename
        self.ownerID = ownerID
        self.receiverAddrList = receiverAddrList

    def getFilename(self):
        return self.filename

    def getOwnerID(self):
        return self.ownerID

    def getReceiverAddr(self):
        return self.receiverAddrList
