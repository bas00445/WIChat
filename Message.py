import time

class Message:
    def __init__(self, text):
        self.text = text

    def getText(self):
        return self.text

    def getCurrentTime(self):
        return str(time.ctime(time.time()))
