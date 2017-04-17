import time
from datetime import datetime

class Message:
    def __init__(self, text, receiverAddrList, memberToSeeMessage, ownerInfo, **kwargs):
        self.text = text
        self.receiverAddr = receiverAddrList
        self.memberToSeeMessage = memberToSeeMessage
        self.ownerInfo = ownerInfo
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


    def getCurrentTime(self):
        s = str(datetime.now())
        s = s[0:len(s)-7]
        return s

    def getMember(self):
        return self.memberToSeeMessage

