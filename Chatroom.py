class Chatroom:
    def __init__(self, roomName):
        self.roomName = roomName
        self.msgCollector = [] ## Message obj
        self.fileCollector = []  ## File obj
        self.memberList = [] ## ClientName

    def getRoomName(self):
        return self.roomName

    def getMsgCollector(self):
        return self.msgCollector

    def getFileCollector(self):
        return self.fileCollector

    def getMemberList(self):
        return self.memberList

    def setRoomName(self, name):
        self.roomName = name

    def addMessage(self, msgObject):
        self.msgCollector.append(msgObject)

    def addFile(self, fileObject):
        self.fileCollector.append(fileObject)

    def addMember(self, newMember):
        self.memberList.append(newMember)

    def __str__(self):
        s = "Room name: " + self.roomName + "\n"
        s += "Member: \n"
        for member in self.memberList:
            s += "\t" + member + "\n"

        return s

    def showAllMessageHistory(self):
        pass

