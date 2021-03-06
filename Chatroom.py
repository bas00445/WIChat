class Chatroom:
    def __init__(self, roomName, creatorID = None, rType = "private", **kwargs):
        self.roomName = roomName
        self.creatorID = creatorID
        self.rType = rType
        self.msgCollector = [] ## Message obj
        self.fileCollector = []  ## File obj
        self.memberNameList = [] ## ClientName
        self.memberIDList = []  ## ClientName
        self.lengthOfData = 0

    def getLengthOfData(self):
        return self.lengthOfData

    def getWidgetCollector(self):
        return self.widgetCollector

    def getRoomName(self):
        return self.roomName

    def getCreatorID(self):
        return self.creatorID

    def getRoomType(self):
        return self.rType

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

    def setRoomID(self, roomID):
        self.roomID = roomID

    def addWidget(self, widget):
        self.widgetCollector.append(widget)

    def addMessage(self, msgObject):
        self.msgCollector.append(msgObject)
        self.lengthOfData += 1

    def addFile(self, fileObject):
        self.fileCollector.append(fileObject)
        self.lengthOfData += 1

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

