import random

class ChatroomCollector:
    def __init__(self, **kwargs):
        self.chatroomList = []
        self.roomIDs = []

    def getRoomByRoomName(self, roomName, creatorID):
        # For single chat
        for room in self.chatroomList:
            if room.getRoomType() == "group":
                if ( room.getRoomName() == roomName and
                     room.getCreatorID() == creatorID ):

                    return room


    def getRoomByMemberName(self, memberNameList):
        for room in self.chatroomList:
            if set(room.getMemberNameList()) == set(memberNameList):
                return room

    def getRoomByMemberID(self, memberIDList):
        for room in self.chatroomList:
            if room.getRoomType() == "single":
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

    def isExist(self, gname, creatorID):
        for room in self.chatroomList:
            if ( room.getRoomName() == gname and
                 room.getCreatorID() == creatorID ):
                return True
        return False