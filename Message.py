import time

class Message:
    def __init__(self, text, receiverAddrList, memberToSeeMessage,  **kwargs):
        self.text = text
        self.receiverAddr = receiverAddrList
        self.memberToSeeMessage = memberToSeeMessage
        self.currentTime = self.getCurrentTime()

    def getText(self):
        return self.text

    def getReceiverAddr(self):
        return self.receiverAddr

    def getCurrentTime(self):
        return str(time.ctime(time.time()))

    def getMember(self):
        return self.memberToSeeMessage

    def __str__(self):
        return self.text + "\n" + self.currentTime
