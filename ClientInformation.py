class ClientInformation:
    def __init__(self, name, status, address, profilePicture, task="", **kwargs):
        self.id = address[1]
        self.name = name
        self.status = status
        self.address = address
        self.profilePicture = profilePicture
        self.task = task
        self.message = ""

    def setTask(self, newTask):
        self.task = newTask

    def setMessage(self, newMsg):
        self.message = newMsg

    def setName(self, name):
        self.name = name

    def setStatus(self, newStatus):
        self.status = newStatus

    def setProfilePic(self, newPic):
        self.profilePicture = newPic

    def getID(self):
        return str(self.id)

    def getTask(self):
        return self.task

    def getName(self):
        return self.name

    def getStatus(self):
        return self.status

    def getProfilePic(self):
        return self.profilePicture

    def getMessage(self):
        return self.message

    def getAddress(self):
        return self.address

    def __str__(self):
        return self.name + " , id: " + str(self.address)


