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
from kivy.uix.widget import Widget
from kivy.uix.carousel import Carousel
from kivy.uix.scatter import Scatter
from kivy.properties import ObjectProperty, StringProperty
#from csvdb.csvdroid_db import build_db
#from csconnector import CsComic,ComicStream
from kivy.logger import Logger
from kivy.lang import Factory

from kivy.loader import Loader
from kivy.uix.carousel import Carousel
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window

import os.path


class ComicCarousel(Carousel):
   pass


class ComicImage(Image):
    def __init__(self, **kwargs):
        self._index = kwargs.pop('_index',0)
        self._thumb = Image()
       # self.page_tb_inrgrid =PageThumbInnerGrid(id=str(self._index))
        super(ComicImage, self).__init__(**kwargs)
    def _image_downloaded(self,  proxyImage,):
        '''Fired once the image is downloaded and ready to use'''
        if proxyImage.image.texture:
            app = App.get_running_app()
            self.texture = proxyImage.image.texture
            if proxyImage.image.texture.width > 2*Window.width:
                self.size_hint = (2,1)
            #this is here in case decide to fix image splitting...
                #right now app is just increase the size of carousel for double pages by 2, below
                #code splits it into 2 seperate images. Have to figure out way to fix thumbs

            #     print "ypu id=%s"%str(app.root.ids['comicscreenid'].ids)
            #     self.texture = proxyImage.image.texture
            #     c_width = self.texture.width
            #     c_height = self.texture.height
            #     part_1 = Image()
            #     part_1_thumb = Image()
            #     part_2 = Image()
            #     part_2_thumb = Image()
            #
            #     part_1.texture = proxyImage.image.texture.get_region(0,0,c_width/2,c_height)
            #     part_2.texture = proxyImage.image.texture.get_region((c_width/2+1),0,c_width/2,c_height)
            #     self.texture = part_1.texture
            #     print 'self_index=%s'%self._index
            #     app.root.ids['comicscreenid'].ids['my_carousel'].add_widget(part_2,self._index+1)
            # else:
            #     self.texture = proxyImage.image.texture


    def _abort_download(self, dt):
        '''Stop the image from downloading'''
        Loader.stop()


class ComicScreen(Screen):
    def __init__(self,**kwargs):
        super(ComicScreen, self).__init__(**kwargs)
    def comicscreen_open_pagescroll_popup(self):
        self.thumb_pop.open()

class ComicScatter(ScatterLayout):
    def __init__(self, **kwargs):
        self.zoom_state = 'normal'
        super(ComicScatter, self).__init__(**kwargs)


    def on_touch_down(self, touch):
        if touch.is_double_tap:
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

class PageThumbImage(ButtonBehavior,AsyncImage):
    def click(self,instance):
        app = App.get_running_app()
        app.root.manager.current = 'comicscreen'
        app.root.ids.comicscreenid.ids['my_carousel'].index = int(instance.id)

class PageThumbSmallButton(Button):
    pass
class PageThumbInnerGrid(GridLayout):
    pass
class PageThumbPop(Popup):
    pass

class PageThumbOutterGrid(GridLayout):
    pass