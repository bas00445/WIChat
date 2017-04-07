class Contact:
    def __init__(self, name, status, id, **kwargs):
        self.name = name
        self.status = status
        self.id = id

    def getName(self):
        return self.name

    def getStatus(self):
        return self.status

    def getID(self):
        return self.id

    def __str__(self):
        return "id: " + str(self.id) +  ", " + self.name + ", state: " + self.status