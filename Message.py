import time

class Message:
    def __init__(self, text, receiverAddr, **kwargs):
        self.text = text
        self.receiverAddr = receiverAddr

    def getText(self):
        return self.text

    def getReceiverAddr(self):
        return self.receiverAddr

    def getCurrentTime(self):
        return str(time.ctime(time.time()))

    def __str__(self):
        return "Text: " + self.text + "\n" + "\t" + self.getCurrentTime()
