import time
from datetime import datetime

class Message:
    def __init__(self, text, receiverAddrList, memberToSeeMessage, ownerName, **kwargs):
        self.text = text
        self.receiverAddr = receiverAddrList
        self.memberToSeeMessage = memberToSeeMessage
        self.ownerName = ownerName
        self.currentTime = self.getCurrentTime()

    def getOwner(self):
        return self.ownerName

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

