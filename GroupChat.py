
class GroupChat:
    def __init__(self, groupID, groupName, **kwargs):
        self.groupID = groupID
        self.groupName = groupName
        self.memberIDs = []

    def addMemberByID(self, id):
        self.memberIDs.append(id)

    def getGroupID(self):
        return self.groupID

    def getGroupName(self):
        return self.groupName
