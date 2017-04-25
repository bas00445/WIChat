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


Builder.load_string('''



<ImageTest>:

    orientation: 'vertical'

    Label:
        canvas.before:
            Color:
                rgba: 0.027, 0.412, 0.698, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Image:
            size: root.size
            pos: root.pos
            source: 'brightPic.jpg'

''')

class ImageTest(BoxLayout):
    pass


class ImageTestApp(App):
    def build(self):
        return ImageTest()

ImageTestApp().run()