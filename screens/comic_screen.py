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


class ComicImage(AsyncImage):
    pass

class ComicScreen(Screen):
 pass

class PageImage(ButtonBehavior,AsyncImage):
    def __init__(self, **kwargs):
        super(PageImage, self).__init__(**kwargs)

    def click(self,instance):
        app = App.get_running_app()
        app.root.manager.current = 'comicscreen'
        app.root.ids.comicscreenid.ids['my_carousel'].index = int(instance.id)


class ComicScatter(ScatterLayout):
    def __init__(self, **kwargs):
        self.zoom_state = 'normal'
        super(ComicScatter, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            print self.id
            if self.zoom_state == 'zoomed':
                self.zoom_state = 'normal'
                mat = self.transform_inv
                self.apply_transform(mat,anchor=(0,0))
            elif self.zoom_state == 'normal':
                self.zoom_state = 'zoomed'
                mat = Matrix().scale(2,2,2)
                self.apply_transform(mat,anchor=touch.pos)
        return super(ComicScatter, self).on_touch_down(touch)
    def on_transform_with_touch(self,touch):
         self.zoom_state = 'zoomed'
         return super(ComicScatter, self).on_transform_with_touch(touch)