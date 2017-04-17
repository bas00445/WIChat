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
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.carousel import Carousel
from kivy.uix.popup import Popup
from kivy.uix.label import Label

#####################################
global WIApp

from ServerSocket import *
from ClientSocket import *
from ClientInformation import *
from Task import *
from Chatroom import *
from ChatroomCollector import *

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
        WIApp.chatroomScreen.updateMsg_thread.start()

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
        time.sleep(0.03)
        task = WIApp.clientSocket.getDataIncome()  ### Can have multiple types of task -> Use if-else

        if task != None and task.getName() == "Request ClientInfo":
            if task.getData() != None:
                WIApp.clientInfoList = task.getData()
                for client in task.getData():
                    if client.getName() != WIApp.username:
                        c = ContactComponent(client.getID(), client.getName())
                        contactScrollView.add_widget(c)

                WIApp.clientSocket.clearData()

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
        self.updateMsg_thread = threading.Thread(target=self.receiverThread)
        self.msgFontSize = 16
        self.colorMsgText = "000000"
        self.colorPartnerText = self.colorMsgText
        self.colorOwnerText = "ffffff"
        self.colorMsgBackground = (0.894, 0.910, 0.922, 1)
        self.colorOwnerBackground = (0.192, 0.263, 0.592, 1)
        self.colorPartnerBackground = (0.745, 0.945, 0.549, 1)

    def on_enter(self, *args):
        WIApp.clientSocket.setText(self.messageInput.text)
        self.sendMessageTask()
        self.messageInput.focus = True

    def receiverThread(self):
        time.sleep(1)
        while True:
            self.updateMessage()
            time.sleep(0.1)

    def loadDataChatroom(self, room):
        self.messageList = room.getMsgCollector()
        self.chatContainer.clear_widgets()
        self.messageInput.bind(on_text_validate=self.on_enter)

        for msg in self.messageList:
            if msg.getOwnerID() != WIApp.clientInfo.getID():
                messageBox = self.createMessageBox_partner(msg, self.colorPartnerBackground, self.colorMsgBackground, self.msgFontSize)

            elif msg.getOwnerID() == WIApp.clientInfo.getID():
                messageBox = self.createMessageBox_owner(msg, self.colorOwnerBackground, self.colorMsgBackground, self.msgFontSize)

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
            messageBox = self.createMessageBox_owner(msg, self.colorOwnerBackground, self.colorMsgBackground, self.msgFontSize)
            self.chatContainer.add_widget(messageBox)
            historyScrollView = WIApp.mainUIScreen.screenSlider.historyScreen.historyScrollView

            for child in historyScrollView.children:
                if child.idButton.text == WIApp.clientTargetID:
                    historyScrollView.remove_widget(child)

            historyScrollView.add_widget(
                HistoryComponent(WIApp.clientTargetAddress[1], WIApp.clientTargetName, self.messageInput.text))
            historyScrollView.children = historyScrollView.children[::-1]

        self.messageInput.text = ""  ## Clear Message Input


    def createMessageBox_partner(self, msg, colorOwner, colorMsg, fontSize):
        messageBox = BoxLayout(size_hint=(1, None), orientation="horizontal")
        senderButton = Button(text='[color=' + str(self.colorPartnerText) + ']' + msg.getOwnerName() + '[/color]', size_hint=(0.3, 1), markup=True, background_normal='', background_color=colorOwner, font_size=fontSize)
        messageBox.add_widget(senderButton)
        temp = BoxLayout(orientation="vertical")
        textButton = Button(text='[color=' + str(self.colorMsgText) + ']' + msg.getText() + '[/color]', markup=True, background_normal='', background_color=colorMsg, font_size=fontSize)
        timeButton = Button(text='[color=' + str(self.colorMsgText) + ']' + msg.getCurrentTime() + '[/color]', markup=True, background_normal='', background_color=colorMsg, font_size=fontSize)
        temp.add_widget(textButton)
        temp.add_widget(timeButton)
        messageBox.add_widget(temp)

        return messageBox

    def createMessageBox_owner(self, msg, colorOwner, colorMsg, fontSize):
        messageBox = BoxLayout(size_hint=(1, None), orientation="horizontal")
        temp = BoxLayout(orientation="vertical")
        textButton = Button(text='[color=' + str(self.colorMsgText) + ']' + msg.getText() + '[/color]', markup=True, background_normal='', background_color=colorMsg, font_size=fontSize)
        timeButton = Button(text='[color=' + str(self.colorMsgText) + ']' + msg.getCurrentTime() + '[/color]', markup=True, background_normal='', background_color=colorMsg, font_size=fontSize)
        temp.add_widget(textButton)
        temp.add_widget(timeButton)
        messageBox.add_widget(temp)
        senderButton = Button(text='[color=' + str(self.colorOwnerText) + ']' + "You" + '[/color]', size_hint=(0.3, 1), markup=True, background_normal='', background_color=colorOwner, font_size=fontSize)
        messageBox.add_widget(senderButton)

        return messageBox


    def updateMessage(self):
        task = WIApp.clientSocket.getDataIncome()
        if task != None:
            if task.getName() == "Message":
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

                historyScrollView = WIApp.mainUIScreen.screenSlider.historyScreen.historyScrollView

                #### Got the message while talking to another chatroom #####
                for room in WIApp.chatroomCollector.getChatroomList():
                    if set(room.getMemberIDList()) == set(msg.getMemberIDList()):
                        room.addMessage(msg)

                        if set(room.getMemberIDList()) == set(WIApp.currentChatroom.getMemberIDList()):
                            if msg.getOwnerID() != WIApp.clientInfo.getID():
                                messageBox = self.createMessageBox_partner(msg, self.colorPartnerBackground,
                                                                           self.colorMsgBackground, self.msgFontSize)

                            elif msg.getOwnerID() == WIApp.clientInfo.getID():
                                messageBox = self.createMessageBox_owner(msg, self.colorOwnerBackground,
                                                                         self.colorMsgBackground, self.msgFontSize)

                            self.chatContainer.add_widget(messageBox)

                        for child in historyScrollView.children:
                            if child.idButton.text == msg.getOwnerID():
                                historyScrollView.remove_widget(child)

                        historyScrollView.add_widget(
                            HistoryComponent(msg.getOwnerID(), msg.getOwnerName(),
                                             msg.getText()))

                        historyScrollView.children = historyScrollView.children[::-1]

            WIApp.clientSocket.clearData()


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
    def __init__(self, id, name, **kwargs):
        super(BoxLayout, self).__init__(**kwargs)
        self.idButton.text = str(id)
        self.nameButton.text = name


class HistoryComponent(BoxLayout):
    def __init__(self, id, name, lastestMsg, **kwargs):
        super(BoxLayout, self).__init__(**kwargs)
        self.idButton.text = str(id)
        self.nameButton.text = name
        self.lastestMessage.text = lastestMsg


class MessageBox(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxLayout, self).__init__(**kwargs)


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
