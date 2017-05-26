class GroupChatCollector:
    def __init__(self):
        self.groups = []

    def getGroupByGName(self, gname):
        for group in self.groups:
            if group.getGroupName() == gname:
                return group

    def addGroup(self, group):
        self.groups.append(group)
