import kivy
import socket
import threading
import time
import os

from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SwapTransition
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.carousel import Carousel
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import *
from kivy.properties import *

#####################################
global WIApp

from ServerSocket import *
from ClientSocket import *
from ClientInformation import *
from Task import *
from Chatroom import *
from ChatroomCollector import *
from FileObject import *

from kivy.core.window import Window

Window.size = (350, 600)

class StartupScreen(Screen):
    def __init__(self, **kwargs):
        super(StartupScreen, self).__init__(**kwargs)

    def openHostPopup(self):
        notification = BoxLayout(orientation="vertical")
        label = Label(text="Please turn on Hotspot\n    before start hosting", font_size="20dp")
        closeButton = Button(text="Close")
        startHostButton = Button(text="Start Hosting")

        closeButton.size_hint = 1, .3
        startHostButton.size_hint = 1, .3

        notification.add_widget(label)
        notification.add_widget(startHostButton)
        notification.add_widget(closeButton)

        popup = Popup(title='Caution', content=notification, size_hint=(.8, .5), auto_dismiss=True)
        popup.open()

        closeButton.bind(on_press=popup.dismiss)
        startHostButton.bind(on_press=self.startHosting)

    def getInputStartup(self):
        WIApp.username = self.nameInput.text
        WIApp.status = ""
        WIApp.ip = self.ipInput.text
        WIApp.port = int(self.portInput.text)

    def login(self):
        self.getInputStartup()
        self.startClient(WIApp.ip, WIApp.port, WIApp.username)
        WIApp.current = "MainUIScreen"
        WIApp.mainUIScreen.profileArea.idButton.text = WIApp.clientInfo.getID()
        WIApp.mainUIScreen.profileArea.nameButton.text = WIApp.username
        WIApp.mainUIScreen.receiveData_thread.start()

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
        self.receiveData_thread = threading.Thread(target=self.receiveData)
        self.filename = None
        self.tLock = threading.Lock()

    def changeScreen(self, name):
        target_idx = self.listofScreen.index(name)
        self.screenSlider.load_slide(self.screenSlider.slides[target_idx])

    def isNewHisComp(self, container, obj):
        for element in container:
            if element.idButton.text == obj.idButton.text:
                return False
        return True

    def move_to_front(self, key, mylist):
        mylist.remove(key)
        mylist.insert(len(mylist), key)

    ## When send a new message
    def updateHistoryType_1(self, msg):
        historyScrollView = self.screenSlider.historyScreen.historyScrollView
        historyComp = HistoryComponent(WIApp.clientTargetID, WIApp.clientTargetName, msg.getText())

        ## Add a new History component to its scroll view
        if self.isNewHisComp(historyScrollView.children, historyComp) == True:
            historyScrollView.add_widget(historyComp, len(historyScrollView.children))

        ## If it already exist, rotate the lastest to the front
        elif self.isNewHisComp(historyScrollView.children, historyComp) == False:
            for i in range(len(historyScrollView.children)):
                if historyScrollView.children[i].idButton.text == WIApp.clientTargetID:
                    historyScrollView.children[i].lastestMessage.text = msg.getText()
                    self.move_to_front(historyScrollView.children[i], historyScrollView.children)

    ## When got an incoming message
    def updateHistoryType_2(self, msg):
        historyScrollView = self.screenSlider.historyScreen.historyScrollView
        historyComp = HistoryComponent(msg.getOwnerID(), msg.getOwnerName(), msg.getText())

        ## Add a new History component to its scroll view
        if self.isNewHisComp(historyScrollView.children, historyComp) == True:
            historyScrollView.add_widget(historyComp, len(historyScrollView.children))

        ## If it already exist, rotate the lastest to the front
        elif self.isNewHisComp(historyScrollView.children, historyComp) == False:
            for i in range(len(historyScrollView.children)):
                if historyScrollView.children[i].idButton.text == msg.getOwnerID():
                    historyScrollView.children[i].lastestMessage.text = msg.getText()
                    self.move_to_front(historyScrollView.children[i], historyScrollView.children)

    def createNewGroup(self):
        groupScrollView = self.screenSlider.contactScreen.groupScrollView.add_widget(Button(text="Hello", size_hint=(1, None)))

    def receiveData(self):
        contactScrollView = self.screenSlider.contactScreen.contactScrollView

        while True:
            task = WIApp.clientSocket.getDataIncome()
            if task != None:
                if task .getName() == "New Client":
                    self.appendNewContact(task, contactScrollView)

                if task.getName() == "Remove Client":
                    self.removeContact(task, contactScrollView)

                if task.getName() == "Message":
                    WIApp.chatroomScreen.updateMessage(task)

                if task.getName() == "Filename":
                    self.filename = task.getData()
                    print("Main filename: ", task.getData())

                    WIApp.clientSocket.sendTask(Task("Got Filename", None))

                if task.getName() == "Store file":
                    # file = open(self.filename, 'wb')
                    #
                    # data = WIApp.clientSocket.soc.recv(4096)
                    # while data:
                    #     print("Receiving the data...")
                    #     file.write(data)
                    #     data = WIApp.clientSocket.soc.recv(4096)
                    #
                    # file.close()

                    pass

                WIApp.clientSocket.clearData()

            time.sleep(0.1)


    def removeContact(self, task, container):
        id = task.getData()

        for child in container.children:
            if child.idButton.text == str(id):
                container.remove_widget(child)

    def appendNewContact(self, task,  container):
        WIApp.clientInfoList = task.getData()
        container.clear_widgets()

        idx = 0  # Index of contact
        for client in task.getData():
            if client.getName() != WIApp.username:
                c = ContactComponent()
                c.idButton.text = str(client.getID())
                c.nameButton.text = client.getName()
                container.add_widget(c, idx)
                idx += 1

    def searchAddrByName(self, targetName):
        for client in WIApp.clientInfoList:
            if client.getName() == targetName:
                return client.getAddress()

    def setClientTarget(self, targetID, targetName):
        WIApp.clientTargetName = targetName
        WIApp.clientTargetAddress = (WIApp.ip, int(targetID))
        WIApp.clientTargetID = targetID

        WIApp.chatroomScreen.roomName.text = WIApp.username + ":" + targetName + " Chatroom"
        currentRoom = WIApp.chatroomCollector.getRoomByMemberID([WIApp.clientInfo.getID(), targetID])

        if currentRoom not in WIApp.chatroomCollector.getChatroomList():
            WIApp.clientSocket.setTargetAddress(WIApp.clientTargetAddress)
            roomName = WIApp.username + ":" + targetName
            newChatroom = Chatroom(roomName)
            newChatroom.addMemberID(WIApp.clientInfo.getID())
            newChatroom.addMemberID(targetID)
            WIApp.chatroomCollector.addNewChatroom(newChatroom)

        ### Choose the current chatroom to load and save the history chat
        WIApp.currentChatroom = WIApp.chatroomCollector.getRoomByMemberID([WIApp.clientInfo.getID(), targetID])
        WIApp.chatroomScreen.loadDataChatroom(WIApp.currentChatroom)

class ChatroomScreen(Screen):
    def __init__(self, **kwargs):
        super(ChatroomScreen, self).__init__(**kwargs)
        self.messageList = None
        self.msgFontSize = 16
        self.colorMsgText = "000000"
        self.colorPartnerText = self.colorMsgText
        self.colorOwnerText = "ffffff"
        self.colorMsgBackground = (0.894, 0.910, 0.922, 1)
        self.colorOwnerBackground = (0.192, 0.263, 0.592, 1)
        self.colorPartnerBackground = (0.745, 0.945, 0.549, 1)
        self.lengthOfHistoryChat = 0
        self.filePath = None

    def on_enter(self, *args):
        WIApp.clientSocket.setText(self.messageInput.text)
        self.sendMessageTask()
        self.messageInput.focus = True

    def loadDataChatroom(self, room):
        self.messageList = room.getMsgCollector()
        self.chatContainer.clear_widgets()
        self.messageInput.bind(on_text_validate=self.on_enter)

        for msg in self.messageList:
            if msg.getOwnerID() != WIApp.clientInfo.getID():
                messageBox = MessageBoxPartner(msg.getOwnerName(), msg.getText(), msg.getCurrentTime())

            elif msg.getOwnerID() == WIApp.clientInfo.getID():
                messageBox = MessageBoxOwner("YOU", msg.getText(), msg.getCurrentTime())

            self.chatContainer.add_widget(messageBox)

    def sendMessageTask(self):
        if self.messageInput.text == "":
            return None

        msg = Message(self.messageInput.text, [WIApp.clientTargetAddress], [WIApp.clientInfo.getID(), WIApp.clientTargetID],
                      (WIApp.username, WIApp.clientInfo.getID()))
        task = Task("Message", msg)
        WIApp.clientSocket.sendTask(task)

        if WIApp.currentChatroom != None:
            WIApp.currentChatroom.addMessage(msg)

        if self.messageInput.text != "":
            messageBox = MessageBoxOwner("You", msg.getText(), msg.getCurrentTime())
            self.chatContainer.add_widget(messageBox)

            WIApp.mainUIScreen.updateHistoryType_1(msg) ## Update history scroll view when send a new message

        self.messageInput.text = ""  ## Clear Message Input

    def createMessageBox(self, msg, state):
        messageBox = BoxLayout(size_hint=(1, None), orientation="horizontal", height = 150)
        textButton = Button(text='[color=' + str(self.colorMsgText) + ']' + msg.getText() + '[/color]', markup=True,
                            background_normal='', background_color=self.colorMsgBackground, font_size=self.msgFontSize, size_hint_y=0.8)
        timeButton = Button(text='[color=' + str(self.colorMsgText) + ']' + msg.getCurrentTime() + '[/color]',
                            markup=True, background_normal='', background_color=self.colorMsgBackground, font_size=self.msgFontSize / 1.5,
                            size_hint_y=0.2)

        temp = BoxLayout(orientation="vertical")
        temp.add_widget(textButton)
        temp.add_widget(timeButton)

        if state == "partner":
            senderButton = Button(text='[color=' + str(self.colorPartnerText) + ']' + msg.getOwnerName() + '[/color]',
                                  size_hint=(0.3, 1), markup=True, background_normal='', background_color=self.colorPartnerBackground,
                                  font_size=self.msgFontSize)
            messageBox.add_widget(senderButton)
            messageBox.add_widget(temp)

        elif state == "you":
            senderButton = Button(text='[color=' + str(self.colorOwnerText) + ']' + "You" + '[/color]',
                                  size_hint=(0.3, 1), markup=True, background_normal='', background_color=self.colorOwnerBackground,
                                  font_size=self.msgFontSize)
            messageBox.add_widget(temp)
            messageBox.add_widget(senderButton)

        return messageBox

    def updateMessage(self, task):
        msg = task.getData()
        targetName = msg.getOwnerName()
        targetID = msg.getOwnerID()

        currentRoom = WIApp.chatroomCollector.getRoomByMemberID([WIApp.clientInfo.getID(), targetID])
        if currentRoom not in WIApp.chatroomCollector.getChatroomList():
            WIApp.clientSocket.setTargetAddress(WIApp.clientTargetAddress)

            ### Create a new room
            roomName = WIApp.username + ":" + targetName
            newChatroom = Chatroom(roomName)
            newChatroom.addMemberID(WIApp.clientInfo.getID())
            newChatroom.addMemberID(targetID)
            WIApp.chatroomCollector.addNewChatroom(newChatroom)

        if WIApp.currentChatroom == None:
            WIApp.currentChatroom = WIApp.chatroomCollector.getRoomByMemberID([WIApp.clientInfo.getID(), targetID])

        #### Got the message while talking to another chatroom #####
        for room in WIApp.chatroomCollector.getChatroomList():
            if set(room.getMemberIDList()) == set(msg.getMemberIDList()):
                room.addMessage(msg)

                ## If got any message while talking in the selected chatroom
                if set(room.getMemberIDList()) == set(WIApp.currentChatroom.getMemberIDList()):
                    if msg.getOwnerID() != WIApp.clientInfo.getID():
                        messageBox = MessageBoxPartner(msg.getOwnerName(), msg.getText(), msg.getCurrentTime())
                    elif msg.getOwnerID() == WIApp.clientInfo.getID():
                        messageBox = MessageBoxOwner("YOU", msg.getText(), msg.getCurrentTime())
                    self.chatContainer.add_widget(messageBox)

                WIApp.mainUIScreen.updateHistoryType_2(msg)

    def openChooserDialog(self):
        cd = FileChooserDialog()
        popup = Popup(title="Choose a file to send", content=cd, size_hint=(.8, .8), auto_dismiss=True)
        popup.open()

    def selectFile(self, path, filename):
        file = open(os.path.join(path, filename[0]), 'rb')

        fname = os.path.join(path, filename[0])
        fname = fname.split('\\')[-1] ## Use the last index as a filename

        obj = FileObject(fname, WIApp.clientInfo.getID(), [WIApp.clientTargetAddress])
        task = Task("Send File", obj)
        WIApp.clientSocket.sendTask(task)


        # data = file.read(4096)
        # while data:
        #     WIApp.clientSocket.soc.send(data)
        #     data = file.read(4096)
        #
        # file.close()


class FileChooserDialog(BoxLayout):
    pass

class ProfileArea(BoxLayout):
    pass


class MenuBar(BoxLayout):
    pass


class ContactScreen(BoxLayout):
    pass


class HistoryScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxLayout, self).__init__(**kwargs)

    def updateOrderChatList(self):
        pass


class ScreenSlider(Carousel):
    pass


class ContactComponent(BoxLayout):
    def __init__(self, **kwargs):
        BoxLayout.__init__(self)


class HistoryComponent(BoxLayout):
    def __init__(self, id, name, lastestMsg, **kwargs):
        BoxLayout.__init__(self) ## This one must use syntax like this
        self.idButton.text = str(id)
        self.nameButton.text = name
        self.lastestMessage.text = lastestMsg

class MessageBoxOwner(BoxLayout):
    def __init__(self, name, text, time, **kwargs):
        BoxLayout.__init__(self)
        self.senderArea.text = name
        self.textArea.text = text
        self.timeArea.text = time


class MessageBoxPartner(BoxLayout):
    def __init__(self, name, text, time, **kwargs):
        BoxLayout.__init__(self)
        self.senderArea.text = name
        self.textArea.text = text
        self.timeArea.text = time

#########################################################

class WIChat(ScreenManager):
    def __init__(self, **kwargs):
        super(WIChat, self).__init__(**kwargs)
        self.username = ""
        self.ip = ""
        self.port = ""
        self.startupScreen = self.startupScreen
        self.mainUIScreen = self.mainUIScreen
        self.chatroomScreen = self.chatroomScreen
        self.clientInfoList = None  # Friend list
        self.historyInfoList = None
        self.chatroomCollector = ChatroomCollector()
        self.serverSocket = None
        self.clientSocket = None
        self.clientTargetAddress = None
        self.clientInfo = None
        self.currentChatroom = None
        self.clientTargetName = None
        self.clientTargetID = None

class WIChatApp(App):
    def build(self):
        global WIApp
        WIApp = WIChat()

        return WIApp

    def on_pause(self):
        return True


WIChatApp().run()
