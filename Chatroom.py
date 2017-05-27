class Chatroom:
    def __init__(self, roomName):
        self.roomName = roomName
        self.msgCollector = [] ## Message obj
        self.fileCollector = []  ## File obj
        self.memberNameList = [] ## ClientName
        self.memberIDList = []  ## ClientName
        self.widgetCollector = [] ## All widget
        self.lengthOfData = 0

    def getLengthOfData(self):
        return self.lengthOfData

    def getWidgetCollector(self):
        return self.widgetCollector

    def getRoomName(self):
        return self.roomName

    def getMsgCollector(self):
        return self.msgCollector

    def getFileCollector(self):
        return self.fileCollector

    def getMemberNameList(self):
        return self.memberNameList

    def getMemberIDList(self):
        return self.memberIDList

    def setRoomName(self, name):
        self.roomName = name

    def addWidget(self, widget):
        self.widgetCollector.append(widget)

    def addMessage(self, msgObject):
        self.msgCollector.append(msgObject)
        self.lengthOfData += 1

    def addFile(self, fileObject):
        self.fileCollector.append(fileObject)
        self.lengthOfData += 1

    def addMemberName(self, newMemberName):
        self.memberNameList.append(newMemberName)

    def addMemberID(self, newMemberID):
        self.memberIDList.append(newMemberID)

    def removeMsg(self, targetMsg):
        for msg in self.msgCollector():
            if msg.getText() == targetMsg.getText():
                self.msgCollector.remove(msg)

    def __str__(self):
        s = "Room name: " + self.roomName + "\n"
        s += "Member: \n"
        for id in self.memberIDList:
            s += "\t" + id + "\n"

        return s


    def showAllMessageHistory(self):
        pass

