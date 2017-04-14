class ChatroomCollector:
    def __init__(self, **kwargs):
        self.chatroomList = []

    def getRoomByRoomName(self, roomName):
        for room in self.chatroomList:
            if room.getRoomName() == roomName:
                return room

    def getRoomByMember(self, memberList):
        for room in self.chatroomList:
            if set(room.getMemberList()) == set(memberList):
                return room

    def getChatroomList(self):
        return self.chatroomList

    def addNewChatroom(self, newRoom):
        self.chatroomList.append(newRoom)

    def listAllChatroom(self):
        for room in self.chatroomList:
            print(room)