import time

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
        return str(time.ctime(time.time()))

    def getMember(self):
        return self.memberToSeeMessage

    def __str__(self):
        return self.text + "\n" + self.currentTime + "\nFrom: " + self.ownerName
