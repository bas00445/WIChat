class FileObject:
    def __init__(self, filename, fsize, ownerID, receiverAddrList, **kwargs):
        self.filename = filename
        self.fsize = fsize
        self.ownerID = ownerID
        self.receiverAddrList = receiverAddrList

    def getFilename(self):
        return self.filename

    def getFileSize(self):
        return self.fsize

    def getOwnerID(self):
        return self.ownerID

    def getReceiverAddr(self):
        return self.receiverAddrList
