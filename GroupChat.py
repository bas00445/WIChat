
class GroupChat:
    def __init__(self, name, id, **kwargs):
        self.name = name
        self.id = id
        self.clientAddresses = []

    def addClient(self, newClient):
        self.clientAddresses.append(newClient)

    def getName(self):
        return self.name

    def getID(self):
        return self.id
