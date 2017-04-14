import time

class Message:
    def __init__(self, text, receiverAddrList, **kwargs):
        self.text = text
        self.receiverAddr = receiverAddrList
        self.currentTime = self.getCurrentTime()

    def getText(self):
        return self.text

    def getReceiverAddr(self):
        return self.receiverAddr

    def getCurrentTime(self):
        return str(time.ctime(time.time()))

    def __str__(self):
        return self.text + "\n" + self.currentTime
