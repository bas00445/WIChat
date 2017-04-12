import kivy
import socket
import threading
import time

from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.carousel import Carousel
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivy.properties import *

#####################################
global WIApp

from ServerSocket import *
from ClientSocket import *
from Contact import *
from ClientInformation import *
from Task import *

#from kivy.core.window import Window
#Window.size = (350, 600)

class StartupScreen(Screen):
    def __init__(self, **kwargs):
        super(StartupScreen, self).__init__(**kwargs)

    def openHostPopup(self):

        notification = BoxLayout(orientation = "vertical")
        label = Label(text="Please turn on Hotspot before start hosting.", font_size = "20dp")
        closeButton = Button(text="Close")
        startHostButton = Button(text="Start Hosting")

        closeButton.size_hint = 1, .3
        startHostButton.size_hint = 1, .3
        notification.add_widget(label)
        notification.add_widget(startHostButton)
        notification.add_widget(closeButton)

        popup = Popup(title='Caution', content=notification, size_hint=(.6, .5),
                      auto_dismiss=True)
        popup.open()

        closeButton.bind(on_press = popup.dismiss)
        startHostButton.bind(on_press = WIApp.startHosting)

class MainUIScreen(Screen):
    def __init__(self, **kwargs):
        super(MainUIScreen, self).__init__(**kwargs)

        self.listofScreen = ["contact", "history"]
        self.curIndxScreen = 0

    def changeScreen(self, name):
        target_idx = self.listofScreen.index(name)
        self.screenSlider.load_slide(self.screenSlider.slides[target_idx])


class ChatroomScreen(Screen):
    def __init__(self, **kwargs):
        super(ChatroomScreen, self).__init__(**kwargs)
        self.buttonColor = (1,.5,.5,1)
        self.buttonColor2 = (1,.7,.7,1)

    def sendMessage1To1(self, thisClient, targetClient):
        pass

    def sendMessage1ToGroup(self, thisClient, groupID):
        pass

    def updateMessageUI(self):
        if self.messageInput.text != "":
            # messageBox = MessageBox()
            # messageBox.msgButton.text = self.messageInput.text
            # messageBox.dateButton.text = str(time.ctime(time.time()))
            #
            messageBox = Label(text = self.messageInput.text + "\n" + str(time.ctime(time.time())), size_hint = (1, None))
            self.chatContainer.add_widget(messageBox)
            #self.messageInput.text = ""


class ProfileArea(BoxLayout):
    pass

class MenuBar(BoxLayout):
    pass

class ContactScreen(BoxLayout):
    pass

class HistoryScreen(BoxLayout):
    pass

class ScreenSlider(Carousel):
    pass

class ContactComponent(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxLayout, self).__init__(**kwargs)

class MessageBox(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxLayout, self).__init__(**kwargs)


#########################################################

class WIChat(ScreenManager):

    def __init__(self, **kwargs):
        super(WIChat, self).__init__(**kwargs)
        self.username = ""
        self.ip = ""
        self.port =""
        self.startupScreen = self.startupScreen
        self.mainUIScreen = self.mainUIScreen
        self.chatroomScreen = self.chatroomScreen
        self.tLock = threading.Lock()
        self.clientInfoList = []
        self.groupList = []

    def getInputStartup(self):
        self.username = self.startupScreen.nameInput.text
        self.status = ""
        self.ip = self.startupScreen.ipInput.text
        self.port = int(self.startupScreen.portInput.text)

    def login(self):
        self.getInputStartup()
        self.current = "MainUIScreen"
        self.startClient(self.ip, self.port, self.username)
        self.mainUIScreen.profileArea.nameButton.text = self.username

    def startHosting(self, instance):
        self.getInputStartup()
        self.serverSocket = ServerSocket(self.ip, self.port)
        self.serverSocket.start()

    def startClient(self, ip, port, username):
        self.clientSocket = ClientSocket(ip, int(port), username)  ## Start client socket loop
        self.clientSocket.connect()
        self.clientSocket.start()

        ### Send the client information to the server ###
        clientInfo = ClientInformation(username, self.status, self.clientSocket.getAddr(), None)
        initialTask = Task("ClientInfo", clientInfo)
        self.clientSocket.sendTask(initialTask)

    def updateContact(self):
        contactScrollView = self.mainUIScreen.screenSlider.contactScreen.contactScrollView
        contactScrollView.clear_widgets()

        task = self.clientSocket.getDataIncome() ### Can have multiple types of task -> Use if-else

        if task.getName() == "ClientInfo":
            print("Update Contact:", task.getData())
            if task.getData() != None:
                for client in task.getData():
                    c = ContactComponent()
                    c.nameButton.text = client.getName()
                    contactScrollView.add_widget(c)

                self.clientInfoList = task.getData()

    def updateReceivedMsg(self):
        chatContainer = self.chatroomScreen.chatContainer

        task = self.clientSocket.getDataIncome()

        if task.getName() == "Message":
            print("Update Message In Chatroom: ", task.getData())
            if task.getData() != None:
                msgLabel = Label(text = "")

    def setClientTarget(self, targetName):
        for client in self.clientInfoList:
            if client.getName() == targetName:
                targetAddress = client.getAddress()

        print("Target Name: ", targetName)
        print("Target Address: ", targetAddress)

        self.clientSocket.setTargetAddress(targetAddress)

    def sendMessageTask(self):
        msgObject = Message(self.chatroomScreen.messageInput.text)
        task = Task("Message", msgObject)
        self.clientSocket.sendTask(task)

    def updateMessage(self):
        chatContainer = self.chatroomScreen.chatContainer
        task = self.clientSocket.getDataIncome()

        print("updateMessage -> Task Name: ", task.getName())

        if task.getName() == "Message":

            data = task.getData()
            string = data.getText() + "\n" + data.getCurrentTime()
            messageBox = Label(text = string, size_hint=(1, None))
            chatContainer.add_widget(messageBox)


class WIChatApp(App):
    def build(self):
        global WIApp
        WIApp = WIChat()

        return WIApp

    def on_pause(self):
        return True

WIChatApp().run()
