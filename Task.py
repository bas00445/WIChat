
class Task:
    def __init__(self, taskName, data, **kwargs):
        self.taskName = taskName
        self.data = data

    def getName(self):
        return self.taskName

    def getData(self):
        return self.data


