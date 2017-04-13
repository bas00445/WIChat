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

        popup = Popup(title='Caution', content=notification, size_hint=(.6, .5), auto_dismiss=True)
        popup.open()

        closeButton.bind(on_press = popup.dismiss)
        startHostButton.bind(on_press = self.startHosting)

    def getInputStartup(self):
        WIApp.username = self.nameInput.text
        WIApp.status = ""
        WIApp.ip = self.ipInput.text
        WIApp.port = int(self.portInput.text)

    def login(self):
        self.getInputStartup()
        self.startClient(WIApp.ip, WIApp.port, WIApp.username)
        WIApp.current = "MainUIScreen"
        WIApp.mainUIScreen.profileArea.nameButton.text = WIApp.username

    def startHosting(self, instance):
        self.getInputStartup()
        WIApp.serverSocket = ServerSocket(WIApp.ip, WIApp.port)
        WIApp.serverSocket.start()

    def startClient(self, ip, port, username):
        WIApp.clientSocket = ClientSocket(ip, int(port), username)  ## Start client socket loop
        WIApp.clientSocket.connect()
        WIApp.clientSocket.start()

        ### Send the client information to the server ###
        WIApp.clientInfo = ClientInformation(username, WIApp.status, WIApp.clientSocket.getAddr(), None)
        initialTask = Task("Submit ClientInfo", WIApp.clientInfo)
        WIApp.clientSocket.sendTask(initialTask)

class MainUIScreen(Screen):
    def __init__(self, **kwargs):
        super(MainUIScreen, self).__init__(**kwargs)

        self.listofScreen = ["contact", "history"]
        self.curIndxScreen = 0

    def changeScreen(self, name):
        target_idx = self.listofScreen.index(name)
        self.screenSlider.load_slide(self.screenSlider.slides[target_idx])

    def updateContact(self):
        contactScrollView = self.screenSlider.contactScreen.contactScrollView
        contactScrollView.clear_widgets()

        task = Task("Request ClientInfo", None)
        WIApp.clientSocket.sendTask(task)
        time.sleep(0.05)
        task = WIApp.clientSocket.getDataIncome() ### Can have multiple types of task -> Use if-else

        if task.getName() == "Request ClientInfo":
            print("Update Contact:", task.getData())
            if task.getData() != None:
                for client in task.getData():
                    if client.getName() != WIApp.username:
                        c = ContactComponent()
                        c.nameButton.text = client.getName()
                        contactScrollView.add_widget(c)

                WIApp.clientInfoList = task.getData()

        WIApp.clientSocket.clearData()

    def setClientTarget(self, targetName):
        for client in WIApp.clientInfoList:
            if client.getName() == targetName:
                WIApp.clientTargetAddress = client.getAddress()

        print("Target Name: ", targetName)
        print("Target Address: ", WIApp.clientTargetAddress)

        WIApp.clientSocket.setTargetAddress(WIApp.clientTargetAddress)
        WIApp.chatroomScreen.roomName.text = targetName.upper() + "'s chatroom"

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

    def sendMessageTask(self):
        msgObject = Message(self.messageInput.text, WIApp.clientTargetAddress)
        task = Task("Message", msgObject)
        WIApp.clientSocket.sendTask(task)

        self.messageInput.text = "" ## Clear Message Input

    def updateMessage(self):
        chatContainer = self.chatContainer
        task = WIApp.clientSocket.getDataIncome()

        if task != None:
            print("updateMessage -> Task Name: ", task.getName())

            if task.getName() == "Message":
                data = task.getData()
                string = data.getText() + "\n" + data.getCurrentTime()
                messageBox = Label(text = string, size_hint=(1, None))
                chatContainer.add_widget(messageBox)

            WIApp.clientSocket.clearData()


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
        self.clientInfoList = None ## Friend list
        self.groupList = None
        self.serverSocket = None
        self.clientSocket = None
        self.clientTargetAddress = None
        self.clientInfo = None

class WIChatApp(App):

    def build(self):
        global WIApp
        WIApp = WIChat()

        return WIApp

    def on_pause(self):
        return True

WIChatApp().run()
