import random

class ChatroomCollector:
    def __init__(self, **kwargs):
        self.chatroomList = []
        self.roomIDs = []

    def getRoomByRoomName(self, roomName):
        for room in self.chatroomList:
            if room.getRoomName() == roomName:
                return room

    def getRoomByMemberName(self, memberNameList):
        for room in self.chatroomList:
            if set(room.getMemberNameList()) == set(memberNameList):
                return room

    def getRoomByMemberID(self, memberIDList):
        for room in self.chatroomList:
            if set(room.getMemberIDList()) == set(memberIDList):
                return room

    def getChatroomList(self):
        return self.chatroomList

    def addNewChatroom(self, newRoom):
        roomID = random.randint(150,400)
        while roomID in self.roomIDs:
            roomID = random.randint(150, 400)

        newRoom.setRoomID(roomID)
        self.chatroomList.append(newRoom)

    def listAllChatroom(self):
        for room in self.chatroomList:
            print(room)

    def __len__(self):
        return len(self.chatroomList)

    def isEmpty(self):
        if len(self.chatroomList) == 0:
            return True
        return False