__version__ = '1.220005'
DEBUG = True
import kivy
kivy.require('1.8.0')
if DEBUG:
    from kivy.config import Config
    print 'setting windows size'
    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '1024')
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.image import Image,AsyncImage
from settingsjson import settings_json
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from screens.comic_screen import ComicScreen, ComicScatter, PageImage, ComicImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.carousel import Carousel
from kivy.uix.scatter import Scatter
from kivy.properties import ObjectProperty, StringProperty
#from csvdb.csvdroid_db import build_db
#from csconnector import CsComic,ComicStream
from kivy.logger import Logger
from kivy.lang import Factory
from kivy.graphics.transformation import Matrix
import os.path



class RootWidget(FloatLayout):
    def load_comic_screen(self,comic):
        manager = ObjectProperty()
        carousel = self.ids['my_carousel']

        image = Image(source='/Users/gerardwhittey/PycharmProjects/Dev/CSVDriod_Dev/images/2521_P0.jpg',allow_streatch=True,cache=True)
        carousel.add_widget(image)

class TestApp(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    TestApp().run()