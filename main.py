import kivy
import socket
import threading
import time

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

#from kivy.core.window import Window
#Window.size = (350, 600)

class StartupScreen(Screen):
    def __init__(self, **kwargs):
        super(StartupScreen, self).__init__(**kwargs)

    def openHostPopup(self):
        global WIApp

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

    def sendMessage(self):
        if self.messageInput.text != "":
            self.chatContainer.add_widget(Label(text=self.messageInput.text, size_hint=(1,None)))
            self.messageInput.text = ""

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


#########################################################

class WIChat(ScreenManager):
    username = StringProperty()
    ip = StringProperty()
    port = NumericProperty()

    def __init__(self, **kwargs):
        super(WIChat, self).__init__(**kwargs)
        self.startupScreen = self.startupScreen
        self.mainUIScreen = self.mainUIScreen
        self.chatroomScreen = self.chatroomScreen
        self.tLock = threading.Lock()
        self.contactList = []
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

        clientInfo = ClientInformation(username, self.status, self.clientSocket.getAddr(), None)

        self.clientSocket.sendClientInformation(clientInfo)

    def updateContact(self):
        contactScrollView = self.mainUIScreen.screenSlider.contactScreen.contactScrollView
        contactScrollView.clear_widgets()


        data = self.clientSocket.getDataIncome()
        print("Update Contact:", data)

        if data != None:
            for client in self.clientSocket.getDataIncome():
                c = ContactComponent()
                c.nameButton.text = client.getName()
                contactScrollView.add_widget(c)



class WIChatApp(App):
    def build(self):
        global WIApp
        WIApp = WIChat()

        return WIApp

    def on_pause(self):
        return True

WIChatApp().run()
