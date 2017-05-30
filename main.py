import kivy
import socket
import threading
import time
import os

from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import *
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.carousel import Carousel
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import *
from kivy.properties import *
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

#####################################
global WIApp

from ServerSocket import *
from ClientSocket import *
from ClientInformation import *
from Task import *
from Chatroom import *
from ChatroomCollector import *
from FileObject import *
from Invitation import *

from kivy.core.window import Window

Window.size = (350, 600)

class StartupScreen(Screen):
    def __init__(self, **kwargs):
        super(StartupScreen, self).__init__(**kwargs)
        self.popup = None

    def openHostPopup(self):
        notification = BoxLayout(orientation="vertical")
        label = Label(text="Please turn on Hotspot\n    before start hosting", font_size="20sp")
        closeButton = Button(text="Close", background_color=(0.000, 0.361, 0.659, 1))
        startHostButton = Button(text="Start Hosting", background_color=(0.000, 0.361, 0.659, 1))

        closeButton.size_hint = 1, .3
        startHostButton.size_hint = 1, .3

        notification.add_widget(label)
        notification.add_widget(startHostButton)
        notification.add_widget(closeButton)

        self.popup = Popup(title='CAUTION' ,content=notification, size_hint=(.8, .5), auto_dismiss=True, background='pictures/backgroundPopup.png')
        self.popup.open()

        closeButton.bind(on_press=self.popup.dismiss)
        startHostButton.bind(on_press=self.startHosting)

    def getInputStartup(self):
        WIApp.username = self.nameInput.text.upper()
        WIApp.status = ""
        WIApp.ip = self.ipInput.text
        WIApp.port = int(self.portInput.text)

    def login(self):
        try:
            self.getInputStartup()
            self.startClient(WIApp.ip, WIApp.port, WIApp.username)
            WIApp.current = "MainUIScreen"
            WIApp.mainUIScreen.profileArea.idButton.text = WIApp.clientInfo.getID()
            WIApp.mainUIScreen.profileArea.nameButton.text = WIApp.username
            WIApp.mainUIScreen.receiveData_thread.start()
        except OSError:
            popup = Popup(title="ERROR!", content=Label(text="There is no any host in server.", font_size="18sp"), auto_dismiss=True, size_hint=(0.8, 0.2),
                          background='pictures/backgroundPopup.png', title_size='20sp')
            popup.open()

    def startHosting(self, instance):
        self.getInputStartup()
        WIApp.serverSocket = ServerSocket(WIApp.ip, WIApp.port)
        WIApp.serverSocket.start()
        self.popup.dismiss()
        self.login()

    def startClient(self, ip, port, username):
        WIApp.clientSocket = ClientSocket(ip, int(port), username)  # Start client socket loop
        WIApp.clientSocket.connect()

        # Send the client information to the server
        WIApp.clientInfo = ClientInformation(username, WIApp.status, WIApp.clientSocket.getAddr(), None)
        initialTask = Task("Submit ClientInfo", WIApp.clientInfo)
        WIApp.clientSocket.sendTask(initialTask)

class InAppNotification(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxLayout, self).__init__(**kwargs)

class MainUIScreen(Screen):
    def __init__(self, **kwargs):
        super(MainUIScreen, self).__init__(**kwargs)
        self.listofScreen = ["contact", "history", "request"]
        self.receiveData_thread = threading.Thread(target=self.receiveData)
        self.filename = None
        self.filePath = None
        self.fileSize = None
        self.messageSound = True
        self.inviteSound = True
        self.sound_msg = SoundLoader.load('sounds/messageSound.mp3')
        self.sound_invite = SoundLoader.load('sounds/inviteSound.mp3')

    def openStatusInput(self):
        container = BoxLayout(orientation='vertical')
        self.statusInput = TextInput(multiline=False)
        confirmButton = Button(text='Confirm', background_color=(0.000, 0.361, 0.659, 1))
        container.add_widget(self.statusInput)
        container.add_widget(confirmButton)
        popup = Popup(title='Input your status', content=container, title_size='20sp',
                      auto_dismiss=True, size_hint=(.7, .2), background='pictures/backgroundPopup.png')
        popup.open()
        confirmButton.bind(on_press=self.changeStatus)

    def changeStatus(self, instance):
        status = self.statusInput.text[:20]
        self.profileArea.statusButton.text = status
        WIApp.clientInfo.setStatus(status)
        task = Task("Change Status", WIApp.clientInfo)
        WIApp.clientSocket.sendTask(task)


    def updateContactStatus(self, task, contactContainer):
        clientInfo = task.getData()
        id = clientInfo.getID()
        name = clientInfo.getName()
        newStatus = clientInfo.getStatus()

        for child in contactContainer.children:
            if child.idButton.text == id and child.nameButton.text == name:
                child.statusButton.text = newStatus


    def changeScreen(self, name):
        target_idx = self.listofScreen.index(name)
        self.screenSlider.load_slide(self.screenSlider.slides[target_idx])

    def showNotification(self, title, detail):
        self.inAppNotification.title.text = title
        self.inAppNotification.detail.text = detail

        anim = Animation(pos=(0, self.height-self.inAppNotification.height), duration=0.25)
        anim.start(self.inAppNotification)

        Clock.schedule_once(self.hideNotification, 3)

    def hideNotification(self, data):
        anim = Animation(pos=(-self.width, self.height - self.inAppNotification.height), duration=0.25)
        anim.start(self.inAppNotification)

    def moveto_chatroom(self, id, name):
        WIApp.transition = SlideTransition(direction="up")
        WIApp.current = "ChatroomScreen"
        self.setClientTarget(id, name)

    def moveto_groupchat(self, gname, creatorID):
        WIApp.transition = SlideTransition(direction="up")
        WIApp.current = "GroupChatScreen"
        WIApp.groupchatScreen.roomName.text = gname
        WIApp.groupchatScreen.roomCreatorID = creatorID
        WIApp.currentChatroom = WIApp.chatroomCollector.getRoomByRoomName(gname, creatorID)
        WIApp.groupchatScreen.loadDataGroupChatroom(WIApp.currentChatroom)

    def moveto_createGroup(self):
        WIApp.transition = SlideTransition(direction="up")
        WIApp.current = "CreateGroupScreen"
        WIApp.createGroupScreen.listAllContact()

    def isNewHisComp(self, container, obj):
        for element in container:
            if isinstance(element, HistoryComponent) and isinstance(obj, HistoryComponent):
                if element.idButton.text == obj.idButton.text:
                    return False
            elif isinstance(element, HistoryGroupComponent) and isinstance(obj, HistoryGroupComponent):
                if ( element.gnameButton.text == obj.gnameButton.text and
                     element.creatorID.text == obj.creatorID.text):
                    return False
        return True

    def sortContactByName(self):
        contactScrollView = self.screenSlider.contactScreen.contactScrollView
        for i in range(len(contactScrollView.children) - 1):
            for j in range(len(contactScrollView.children) - 1):
                if contactScrollView.children[j].nameButton.text < contactScrollView.children[j + 1].nameButton.text:
                    temp = contactScrollView.children[j]
                    contactScrollView.children[j] = contactScrollView.children[j + 1]
                    contactScrollView.children[j+1] = temp

    # Move the key to front fron the list
    def move_to_front(self, key, mylist):
        mylist.remove(key)
        mylist.insert(len(mylist), key)

    # When send a new message
    def updateHistoryType_1(self, msg):
        historyScrollView = self.screenSlider.historyScreen.historyScrollView

        if msg.getGroupName() == None:
            historyComp = HistoryComponent(WIApp.clientTargetID, WIApp.clientTargetName, msg.getText())

        elif msg.getGroupName() != None:
            historyComp = HistoryGroupComponent(msg.getGroupName(), msg.getRoomCreatorID(), msg.getText())

        # Add a new History component to its scroll view
        if self.isNewHisComp(historyScrollView.children, historyComp) == True:
            historyScrollView.add_widget(historyComp, len(historyScrollView.children))

        # If it already exist, rotate the lastest to the front
        elif self.isNewHisComp(historyScrollView.children, historyComp) == False:
            for i in range(len(historyScrollView.children)):
                if isinstance(historyScrollView.children[i], HistoryComponent):
                    if ( historyScrollView.children[i].idButton.text == msg.getReceiverAddr()[0]
                         and msg.getGroupName() == None ):
                        historyScrollView.children[i].lastestMsg.text = msg.getText()
                        self.move_to_front(historyScrollView.children[i], historyScrollView.children)

                elif isinstance(historyScrollView.children[i], HistoryGroupComponent):
                    if ( historyScrollView.children[i].gnameButton.text == msg.getGroupName() and
                         historyScrollView.children[i].creatorID.text == msg.getRoomCreatorID()):
                        historyScrollView.children[i].lastestMsg.text = msg.getText()
                        self.move_to_front(historyScrollView.children[i], historyScrollView.children)

    # When got an incoming message
    def updateHistoryType_2(self, msg):
        historyScrollView = self.screenSlider.historyScreen.historyScrollView

        if msg.getGroupName() == None:
            historyComp = HistoryComponent(msg.getOwnerID(), msg.getOwnerName(), msg.getText())

        if msg.getGroupName() != None:
            historyComp = HistoryGroupComponent(msg.getGroupName(), msg.getRoomCreatorID(), msg.getText())

        # Add a new History component to its scroll view
        if self.isNewHisComp(historyScrollView.children, historyComp) == True:
            historyScrollView.add_widget(historyComp, len(historyScrollView.children))

        # If it already exist, rotate the lastest to the front
        elif self.isNewHisComp(historyScrollView.children, historyComp) == False:
            for i in range(len(historyScrollView.children)):
                if isinstance(historyScrollView.children[i], HistoryComponent):
                    if historyScrollView.children[i].idButton.text == msg.getOwnerID() and msg.getGroupName() == None:
                        historyScrollView.children[i].lastestMsg.text = msg.getText()
                        self.move_to_front(historyScrollView.children[i], historyScrollView.children)

                elif isinstance(historyScrollView.children[i], HistoryGroupComponent):
                    if ( historyScrollView.children[i].gnameButton.text == msg.getGroupName() and
                         historyScrollView.children[i].creatorID.text == msg.getRoomCreatorID()):

                        historyScrollView.children[i].lastestMsg.text = msg.getText()
                        self.move_to_front(historyScrollView.children[i], historyScrollView.children)

    def sendGroupInformation(self, groupChat):
        task = Task("Update Group Members", groupChat)
        WIApp.clientSocket.sendTask(task)

    def updateGroupMembers(self, task):
        groupObj = task.getData()
        gname = groupObj.getRoomName()
        creatorID = groupObj.getCreatorID()

        currentGroup = WIApp.chatroomCollector.getRoomByRoomName(gname, creatorID)

        gmemberID = groupObj.getMemberIDList()
        currentGroupID = currentGroup.getMemberIDList()

        difference = set(gmemberID).difference(set(currentGroupID))
        while len(difference) != 0:
            currentGroup.addMemberID(difference.pop())

    def receiveData(self):
        contactScrollView = self.screenSlider.contactScreen.contactScrollView
        inviteScrollView = WIApp.createGroupScreen.contactContainer

        while True:
            data = WIApp.clientSocket.getDataIncome()
            if data != None:
                try:
                    task = pickle.loads(data)
                    if task.getName() == "New Client":
                        self.appendNewContact(task, contactScrollView, inviteScrollView)

                    if task.getName() == "Remove Client":
                        self.removeContact(task, contactScrollView, inviteScrollView)

                    if task.getName() == "Change Status":
                        self.updateContactStatus(task, contactScrollView)

                    if task.getName() == "Invite to group":
                        inviteObj = task.getData()
                        title = "Invitation"
                        ownerName = inviteObj.getOwnerInfo().getName()
                        detail = ownerName + " invite to group: " + inviteObj.getGroupName()
                        detail = detail[:20]
                        requestContainer = self.screenSlider.requestScreen.requestContainer
                        requestContainer.add_widget(RequestComponent(inviteObj.getOwnerInfo().getID(),
                                                                     inviteObj.getOwnerInfo().getName(),
                                                                     inviteObj.getGroupName()))
                        if WIApp.current == "MainUIScreen":
                            self.showNotification(title, detail)

                        if WIApp.current == "ChatroomScreen":
                            WIApp.chatroomScreen.showNotificationChatroom(title, detail)

                        if WIApp.current == "GroupChatScreen":
                            WIApp.groupchatScreen.showNotificationChatroom(title, detail)

                        if self.inviteSound == True:
                            self.sound_invite.play()

                    if task.getName() == "Response Invitation":
                        inviteObj = task.getData()
                        if inviteObj.getResponse() == "accept":
                            gname = inviteObj.getGroupName()
                            ownerID = inviteObj.getOwnerInfo().getID()
                            groupChatRoom = WIApp.chatroomCollector.getRoomByRoomName(gname, WIApp.clientInfo.getID())
                            groupChatRoom.addMemberID(ownerID)
                            self.sendGroupInformation(groupChatRoom)

                    if task.getName() == "Message":
                        WIApp.chatroomScreen.updateMessage(task)
                        msgObj = task.getData()
                        ownerName = msgObj.getOwnerName()
                        detail = msgObj.getText()
                        detail = detail[:20]

                        if WIApp.current == "MainUIScreen":
                            self.showNotification(ownerName, detail)

                        if WIApp.current == "ChatroomScreen":
                            WIApp.chatroomScreen.showNotificationChatroom(ownerName, detail)

                        if WIApp.current == "GroupChatScreen":
                            WIApp.groupchatScreen.showNotificationChatroom(ownerName, detail)

                        if self.messageSound == True:
                            self.sound_msg.play()

                    if task.getName() == "Group Message":
                        WIApp.groupchatScreen.updateGroupMessage(task)

                        msgObj = task.getData()
                        gName = msgObj.getGroupName()
                        detail = msgObj.getText()
                        detail = detail[:20]

                        if WIApp.current == "MainUIScreen":
                            self.showNotification(gName, detail)

                        if WIApp.current == "ChatroomScreen":
                            WIApp.chatroomScreen.showNotificationChatroom(gName, detail)

                        if WIApp.current == "GroupChatScreen":
                            WIApp.groupchatScreen.showNotificationChatroom(gName, detail)

                        if self.messageSound == True:
                            self.sound_msg.play()

                    if task.getName() == "Update Group Members":
                        self.updateGroupMembers(task)

                    if task.getName() == "FileDetail":
                        fileObj = task.getData()
                        self.filename = fileObj.getFilename()
                        self.fileSize = fileObj.getFileSize()
                        self.filePath = "clientFiles/" + self.filename

                        self.requestFileData


                    WIApp.clientSocket.clearData()

                except OverflowError:
                    pass
                except ValueError:
                    pass
                except KeyError:
                    pass
                except EOFError:
                    pass
                except pickle.UnpicklingError:
                    pass
                except pickle.PicklingError:
                    pass
                except pickle.PickleError:
                    pass

            time.sleep(0.1)

    def removeContact(self, task, container1, container2):
        id = task.getData()

        # Remove ContactComponent
        for x in container1.children:
            if x.idButton.text == str(id):
                container1.remove_widget(x)

        # Remove InviteComponent
        for y in container2.children:
            if y.idButton.text == str(id):
                print("remove Invite")
                container2.remove_widget(y)

    def appendNewContact(self, task,  container1, container2):
        WIApp.clientInfoList = task.getData()
        container1.clear_widgets()

        idx = 0
        for x in WIApp.clientInfoList:
            if x.getID() != WIApp.clientInfo.getID():
                c = ContactComponent(x.getID(), x.getName())
                container1.add_widget(c, idx)
                idx += 1

        idx = 0
        for x in WIApp.clientInfoList:
            if x.getID() != WIApp.clientInfo.getID():
                c = InviteComponent()
                c.idButton.text = str(x.getID())
                c.nameButton.text = x.getName()
                container2.add_widget(c, idx)
                idx += 1

    def searchAddrByName(self, targetName):
        for client in WIApp.clientInfoList:
            if client.getName() == targetName:
                return client.getAddress()

    def setClientTarget(self, targetID, targetName):
        WIApp.clientTargetName = targetName
        WIApp.clientTargetID = targetID

        WIApp.chatroomScreen.roomName.text = WIApp.username + " and " + targetName
        currentRoom = WIApp.chatroomCollector.getRoomByMemberID([WIApp.clientInfo.getID(), targetID])

        if currentRoom not in WIApp.chatroomCollector.getChatroomList():
            roomName = WIApp.username + " and " + targetName
            newChatroom = Chatroom(roomName, rType="single")
            newChatroom.addMemberID(WIApp.clientInfo.getID())
            newChatroom.addMemberID(targetID)
            WIApp.chatroomCollector.addNewChatroom(newChatroom)

        # Choose the current chatroom to load and save the history chat
        WIApp.currentChatroom = WIApp.chatroomCollector.getRoomByMemberID([WIApp.clientInfo.getID(), targetID]) ## Load private chat
        WIApp.chatroomScreen.loadDataChatroom(WIApp.currentChatroom)

class InviteComponent(BoxLayout):
    def __init__(self,**kwargs):
        super(BoxLayout, self).__init__(**kwargs)

    def isSelected(self):
        return self.selection.active

class RequestComponent(BoxLayout):
    def __init__(self, id, name, groupname, **kwargs):
        BoxLayout.__init__(self, **kwargs)
        self.idButton.text = str(id)
        self.nameButton.text = name
        self.groupButton.text = groupname

class CreateGroupScreen(Screen):
    def __init__(self, **kwargs):
        super(CreateGroupScreen, self).__init__(**kwargs)

    def listAllContact(self):
        self.contactContainer.clear_widgets()
        idx = 0
        for client in WIApp.clientInfoList:
            if client.getID() != WIApp.clientInfo.getID():
                ic = InviteComponent()
                ic.idButton.text = str(client.getID())
                ic.nameButton.text = client.getName()
                self.contactContainer.add_widget(ic, idx)
                idx += 1

    def removeContact(self):
        pass

    def moveto_mainUI(self):
        WIApp.transition = SlideTransition(direction="right")
        WIApp.current = "MainUIScreen"

    def sendInvitation(self):
        gname = self.groupNameInput.text
        creatorID = WIApp.clientInfo.getID()

        if len(gname) == 0 or not gname.isalpha():
            popup = Popup(title='Invalid Group Name', content=Label(text="Group name must be alphabet!"),
                          auto_dismiss=True, size_hint=(.7,.2), background='pictures/backgroundPopup.png')
            popup.open()
            return None

        if len(self.contactContainer.children) == 0:
            popup = Popup(title='ERROR', content=Label(text="There is no client in server!"),
                          auto_dismiss=True, size_hint=(.7, .2), background='pictures/backgroundPopup.png')
            popup.open()
            return None

        if WIApp.chatroomCollector.isExist(gname, creatorID):
            popup = Popup(title='Invalid Group Name', content=Label(text="This name already exist!"),
                          auto_dismiss=True, size_hint=(.7, .2), background='pictures/backgroundPopup.png')
            popup.open()
            return None

        receivedAddrs = []
        for invc in self.contactContainer.children:
            if invc.isSelected() == True:
                receivedAddrs.append(invc.idButton.text)

        inviteObj = Invitation(receivedAddrs, WIApp.clientInfo, self.groupNameInput.text)
        task = Task("Invite to group", inviteObj)

        # Create widget #
        gname = self.groupNameInput.text
        group = Chatroom(gname, WIApp.clientInfo.getID(), rType="group")
        group.addMemberID(inviteObj.getOwnerInfo().getID())  ## Attach id of sender
        WIApp.chatroomCollector.addNewChatroom(group)

        groupWidget = GroupChatComponent(gname, inviteObj.getOwnerInfo().getID(),
                                                inviteObj.getOwnerInfo().getName())

        groupContainer = WIApp.mainUIScreen.screenSlider.contactScreen.groupContainer
        groupContainer.add_widget(groupWidget)

        WIApp.clientSocket.sendTask(task)

class GroupChatComponent(BoxLayout):
    def __init__(self, gname, creatorID, creatorName, **kwargs):
        BoxLayout.__init__(self)
        self.gnameButton.text = gname
        self.creatorID.text = creatorID
        self.creatorName.text = "Creator: " + creatorName

class HistoryGroupComponent(BoxLayout):
    def __init__(self, gname, creatorID, lastestMsg, **kwargs):
        super(BoxLayout, self).__init__(**kwargs)
        self.gnameButton.text = gname
        self.creatorID.text = creatorID
        self.lastestMsg.text = lastestMsg

class IDContainer(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxLayout, self).__init__(**kwargs)

class GroupChatScreen(Screen):
    def __init__(self, **kwargs):
        super(GroupChatScreen, self).__init__(**kwargs)
        self.filePath = None
        self.roomCreatorID = None

    def backup(self):
        currentRoom = WIApp.currentChatroom
        messages = currentRoom.getMsgCollector()
        filename = currentRoom.getRoomName() + '.txt'
        file = open('backupChat/' + filename, 'w')

        for msg in messages:
            print(msg.getOwnerName())
            if msg.getOwnerID() != WIApp.clientInfo.getID():
                data = msg.getOwnerName() + " @ " + msg.getTimeCreated() + " : " + msg.getText() + "\n"
                file.write(data)

            elif msg.getOwnerID() == WIApp.clientInfo.getID():
                data = "You @ " + msg.getTimeCreated() + " : " + msg.getText() + "\n"
                file.write(data)

        file.close()
        print("Close file")

    def showNotificationChatroom(self, title, detail):
        if title == WIApp.clientTargetName or title == WIApp.groupchatScreen.roomName.text:
            return None

        self.inRoomNotification.title.text = title
        self.inRoomNotification.detail.text = detail

        anim = Animation(pos=(0, self.height - self.inRoomNotification.height), duration=0.25)
        anim.start(self.inRoomNotification)
        Clock.schedule_once(self.hideNotification, 3)

    def listMembers(self):
        idContainer = IDContainer()
        currentRoom = WIApp.chatroomCollector.getRoomByRoomName(self.roomName.text, self.roomCreatorID)
        idList = currentRoom.getMemberIDList()

        for id in idList:
            idContainer.container.add_widget(Label(text= "ID: " + str(id), size_hint_y=None, font_size="18sp"))

        popup = Popup(title="All members:", content=idContainer, auto_dismiss=True, size_hint=(0.7,0.7),
                      background='pictures/backgroundPopup.png', title_size='20sp')
        popup.open()

    def hideNotification(self, data):
        anim = Animation(pos=(-self.width, self.height - self.inRoomNotification.height), duration=0.25)
        anim.start(self.inRoomNotification)

    def sendMessageTask(self, groupname, creatorID):
        if self.messageInput.text == "":
            return None
        groupChat = WIApp.chatroomCollector.getRoomByRoomName(groupname, creatorID)
        receiverAddrs = groupChat.getMemberIDList()

        createdTime = str(datetime.now())
        createdTime = createdTime[0:len(createdTime) - 7]
        msg = Message(self.messageInput.text, receiverAddrs,
                      (WIApp.username, WIApp.clientInfo.getID()), groupname, creatorID, timeCreated=createdTime)

        task = Task("Group Message", msg)
        WIApp.clientSocket.sendTask(task)

        WIApp.currentChatroom = groupChat
        WIApp.currentChatroom.addMessage(msg)

        if self.messageInput.text != "":
            messageBox = MessageBoxOwner("YOU", msg.getText(), msg.getTimeCreated())
            self.groupchatContainer.add_widget(messageBox)

        self.messageInput.text = ""  # Clear Message Input

        WIApp.mainUIScreen.updateHistoryType_1(msg) # Update history scroll view when send a new message

    def loadDataGroupChatroom(self, room):
        self.messageList = room.getMsgCollector()
        self.groupchatContainer.clear_widgets()
        self.messageInput.bind(on_text_validate=self.on_enter)

        for msg in self.messageList:
            if msg.getGroupName() == room.getRoomName():
                if msg.getOwnerID() != WIApp.clientInfo.getID():
                    messageBox = MessageBoxPartner(msg.getOwnerName(), msg.getText(), msg.getTimeCreated())

                elif msg.getOwnerID() == WIApp.clientInfo.getID():
                    messageBox = MessageBoxOwner("YOU", msg.getText(), msg.getTimeCreated())

                self.groupchatContainer.add_widget(messageBox)

    def showMenu(self):
        anim = Animation(pos=(0, 0), duration=.5)
        anim.start(self.menu)

    def hideMenu(self):
        anim = Animation(pos=(-self.width, 0), duration=.5)
        anim.start(self.menu)

    def updateGroupMessage(self, task):
        msg = task.getData()
        gname = msg.getGroupName()
        creatorID = msg.getRoomCreatorID()


        if WIApp.currentChatroom == None:
            WIApp.currentChatroom = WIApp.chatroomCollector.getRoomByRoomName(gname, creatorID)

        # Got the message while talking to another chatroom
        for room in WIApp.chatroomCollector.getChatroomList():
            if room.getRoomName() == gname:
                room.addMessage(msg)

                ## If got any message while talking in the selected chatroom
                if room.getRoomName() == WIApp.currentChatroom.getRoomName():
                    if msg.getOwnerID() != WIApp.clientInfo.getID():
                        messageBox = MessageBoxPartner(msg.getOwnerName(), msg.getText(), msg.getTimeCreated())
                    elif msg.getOwnerID() == WIApp.clientInfo.getID():
                        messageBox = MessageBoxOwner("YOU", msg.getText(), msg.getTimeCreated())

                    self.groupchatContainer.add_widget(messageBox)

                WIApp.mainUIScreen.updateHistoryType_2(msg) # Group

    def openChooserDialog(self):
        cd = FileChooserDialog()
        popup = Popup(title="Choose a file to send", content=cd, size_hint=(.8, .8), auto_dismiss=True)
        popup.open()

    def selectFile(self, path, filename):
        file = open(os.path.join(path, filename[0]), 'rb')

        fname = os.path.join(path, filename[0])
        fsize = os.path.getsize(fname)
        fname = fname.split('\\')[-1] # Use the last index as a filename

        obj = FileObject(fname, fsize, WIApp.clientInfo.getID(), [WIApp.clientTargetID])
        task = Task("Send File", obj)
        WIApp.clientSocket.sendTask(task)

        data = file.read(1024)
        while data:
            print(">>Sending a file<<")
            WIApp.clientSocket.sendData(data)
            data = file.read(1024)

        print("Completed sending file!")
        file.close()


class ChatroomScreen(Screen):
    def __init__(self, **kwargs):
        super(ChatroomScreen, self).__init__(**kwargs)
        self.messageList = None
        self.filePath = None

    def on_enter(self, *args):
        self.hideMenu()

    def backup(self):
        currentRoom = WIApp.currentChatroom
        messages = currentRoom.getMsgCollector()
        filename = currentRoom.getRoomName() + '.txt'
        file = open('backupChat/' + filename, 'w')

        for msg in messages:
            print(msg.getOwnerName())
            if msg.getOwnerID() != WIApp.clientInfo.getID():
                data = msg.getOwnerName() + " @ " + msg.getTimeCreated() + " : " + msg.getText() + "\n"
                file.write(data)

            elif msg.getOwnerID() == WIApp.clientInfo.getID():
                data = "You @ " + msg.getTimeCreated() + " : " + msg.getText() + "\n"
                file.write(data)

        file.close()
        print("Close file")


    def showNotificationChatroom(self, title, detail):
        if title == WIApp.clientTargetName:
            return None

        self.inRoomNotification.title.text = title
        self.inRoomNotification.detail.text = detail

        anim = Animation(pos=(0, self.height - self.inRoomNotification.height), duration=0.25)
        anim.start(self.inRoomNotification)

        Clock.schedule_once(self.hideNotification, 3)


    def hideNotification(self, data):
        anim = Animation(pos=(-self.width, self.height - self.inRoomNotification.height), duration=0.25)
        anim.start(self.inRoomNotification)


    def moveto_mainUI(self):
        WIApp.transition = SlideTransition(direction="right")
        WIApp.current = "MainUIScreen"
        self.hideMenu()

    def loadDataChatroom(self, room):
        self.messageList = room.getMsgCollector()
        self.chatContainer.clear_widgets()
        self.messageInput.bind(on_text_validate=self.on_enter)

        for msg in self.messageList:
            if msg.getOwnerID() != WIApp.clientInfo.getID():
                messageBox = MessageBoxPartner(msg.getOwnerName(), msg.getText(), msg.getTimeCreated())

            elif msg.getOwnerID() == WIApp.clientInfo.getID():
                messageBox = MessageBoxOwner("YOU", msg.getText(), msg.getTimeCreated())

            self.chatContainer.add_widget(messageBox)

    def showMenu(self):
        anim = Animation(pos=(0, 0), duration=.5)
        anim.start(self.menu)

    def hideMenu(self):
        anim = Animation(pos=(-self.width, 0), duration=.5)
        anim.start(self.menu)

    def sendMessageTask(self):
        if self.messageInput.text == "":
            return None
        createdTime = str(datetime.now())
        createdTime = createdTime[0:len(createdTime)-7]
        currentRoom = WIApp.chatroomCollector.getRoomByMemberID([WIApp.clientTargetID, WIApp.clientInfo.getID()])
        WIApp.currentChatroom = currentRoom

        msg = Message(self.messageInput.text, [WIApp.clientTargetID, WIApp.clientInfo.getID()],
                      (WIApp.username, WIApp.clientInfo.getID()), timeCreated=createdTime )
        task = Task("Message", msg)
        WIApp.clientSocket.sendTask(task)
        WIApp.currentChatroom.addMessage(msg)

        if self.messageInput.text != "":
            messageBox = MessageBoxOwner("YOU", msg.getText(), msg.getTimeCreated())
            self.chatContainer.add_widget(messageBox)

            WIApp.mainUIScreen.updateHistoryType_1(msg) # Update history scroll view when send a new message

        self.messageInput.text = ""  # Clear Message Input

    def updateMessage(self, task):
        msg = task.getData()
        targetName = msg.getOwnerName()
        targetID = msg.getOwnerID()
        WIApp.clientTargetID = targetID

        currentRoom = WIApp.chatroomCollector.getRoomByMemberID([WIApp.clientInfo.getID(), targetID])
        if currentRoom not in WIApp.chatroomCollector.getChatroomList():
            # Create a new room
            roomName = WIApp.username + " and " + targetName
            newChatroom = Chatroom(roomName, rType="single")

            newChatroom.addMemberID(WIApp.clientInfo.getID())
            newChatroom.addMemberID(targetID)
            WIApp.chatroomCollector.addNewChatroom(newChatroom)

        if WIApp.currentChatroom == None:
            WIApp.currentChatroom = WIApp.chatroomCollector.getRoomByMemberID([WIApp.clientInfo.getID(), targetID])

        # Got the message while talking to another chatroom
        twice = False
        for room in WIApp.chatroomCollector.getChatroomList():
            if (set(room.getMemberIDList()) == set(msg.getReceiverAddr())
                and not (WIApp.clientInfo.getID() == msg.getOwnerID())):
                room.addMessage(msg)

                # If got any message while talking in the selected chatroom
                if set(room.getMemberIDList()) == set(WIApp.currentChatroom.getMemberIDList()) and not twice:
                    if msg.getOwnerID() != WIApp.clientInfo.getID():
                        messageBox = MessageBoxPartner(msg.getOwnerName(), msg.getText(), msg.getTimeCreated())
                    elif msg.getOwnerID() == WIApp.clientInfo.getID():
                        messageBox = MessageBoxOwner("YOU", msg.getText(), msg.getTimeCreated())

                    self.chatContainer.add_widget(messageBox)
                    twice = True

                WIApp.mainUIScreen.updateHistoryType_2(msg)

    def openChooserDialog(self):
        cd = FileChooserDialog()
        popup = Popup(title="Choose a file to send", content=cd, size_hint=(.8, .8), auto_dismiss=True)
        popup.open()

    def selectFile(self, path, filename):
        file = open(os.path.join(path, filename[0]), 'rb')

        fname = os.path.join(path, filename[0])
        fsize = os.path.getsize(fname)
        fname = fname.split('\\')[-1] # Use the last index as a filename

        obj = FileObject(fname, fsize, WIApp.clientInfo.getID(), [WIApp.clientTargetID])
        task = Task("Send File", obj)
        WIApp.clientSocket.sendTask(task)

        data = file.read(1024)
        while data:
            print(">>Sending a file<<")
            WIApp.clientSocket.sendData(data)
            data = file.read(1024)

        print("Completed sending file!")
        file.close()

class FileChooserDialog(BoxLayout):
    pass

class ProfileArea(BoxLayout):
    pass

class MenuBar(BoxLayout):
    pass

class ContactScreen(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def updateOrderChatList(self):
        pass

class RequestScreen(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def responseInvitation(self, gname, creatorID, creatorName, answer, root):
        inv = Invitation([creatorID], WIApp.clientInfo, gname, answer)
        task = Task("Response Invitation", inv)
        WIApp.clientSocket.sendTask(task)

        if answer == "accept":
            # Create a groupchat widget
            groupWidget = GroupChatComponent(gname, creatorID, creatorName)
            groupContainer = WIApp.mainUIScreen.screenSlider.contactScreen.groupContainer
            groupContainer.add_widget(groupWidget)

            groupChatroom = Chatroom(gname, creatorID, rType="group")
            groupChatroom.addMemberID(creatorID)
            groupChatroom.addMemberID(WIApp.clientInfo.getID())
            WIApp.chatroomCollector.addNewChatroom(groupChatroom)

        self.requestContainer.remove_widget(root) # Remove the request component

class ScreenSlider(Carousel):
    pass

class ContactComponent(BoxLayout):
    def __init__(self, id, name, **kwargs):
        BoxLayout.__init__(self)  # This one must use syntax like this
        self.idButton.text = str(id)
        self.nameButton.text = name


class HistoryComponent(BoxLayout):
    def __init__(self, id, name, lastestMsg, **kwargs):
        BoxLayout.__init__(self) # This one must use syntax like this
        self.idButton.text = str(id)
        self.nameButton.text = name
        self.lastestMsg.text = lastestMsg

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
        self.clientInfoList = None
        self.historyInfoList = None
        self.chatroomCollector = ChatroomCollector()
        self.serverSocket = None
        self.clientSocket = None
        self.clientInfo = None
        self.currentChatroom = None
        self.clientTargetName = None
        self.clientTargetID = None

class WIChatApp(App):
    def build(self):
        global WIApp
        WIApp = WIChat()

        return WIApp

    # App will not be terminated when open other Apps
    def on_pause(self):
        return True


WIChatApp().run()
