import time
from datetime import datetime

class Message:
    def __init__(self, text, receiverAddrList, ownerInfo, groupName = None, **kwargs):
        self.text = text
        self.receiverAddr = receiverAddrList # Socket address of the receiver
        self.ownerInfo = ownerInfo
        self.groupName = groupName
        self.ownerName = ownerInfo[0]
        self.ownerID = ownerInfo[1]
        self.currentTime = self.getCurrentTime()

    def getOwnerInfo(self):
        return self.ownerInfo

    def getOwnerName(self):
        return self.ownerName

    def getOwnerID(self):
        return self.ownerID

    def getText(self):
        return self.text

    def getReceiverAddr(self):
        return self.receiverAddr

    def getGroupName(self):
        return self.groupName

    def getCurrentTime(self):
        s = str(datetime.now())
        s = s[0:len(s)-7]
        return s


