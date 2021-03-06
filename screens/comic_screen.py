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
from kivy.uix.label import Label
from parts import TopActionBar
from kivy.loader import Loader
from kivy.properties import NumericProperty
from kivy.uix.carousel import Carousel
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
import os.path


class ComicCarousel(Carousel):
   pass


class ComicImage(Image):
    def __init__(self, **kwargs):
       # self.page_tb_inrgrid =PageThumbInnerGrid(id=str(self._index))
        super(ComicImage, self).__init__(**kwargs)
        self._index = kwargs.pop('_index',0)
        self._thumb = Image()

    def _image_downloaded(self, widget ,comicstream_number, proxyImage,):
        '''Fired once the image is downloaded and ready to use'''
        if proxyImage.image.texture:
            base_url = App.get_running_app().config.get('Server', 'url')
            src_thumb = "%s/comic/%d/page/%d?max_height=200#.jpg" % (base_url, comicstream_number, self._index)
            app = App.get_running_app()
            inner_grid_id ='inner_grid' + str(self._index)
            page_image_id = str(self._index)
            split_dbl_page = App.get_running_app().config.get('Display', 'dblpagesplit')
            if proxyImage.image.texture.width > 2*Window.width and split_dbl_page == '1':
                m_win_x = Window.width
                m_win_y = Window.height
                self.texture = proxyImage.image.texture
                c_width = self.texture.width
                c_height = self.texture.height
                part_1 = Image()
                part_1_thumb = Image()
                scatter = ComicScatter(do_rotation=False, do_scale=False,do_translation_x=False,
                                       id='comic_scatter'+str(self._index)+'b',scale_min=1, scale_max=2,
                                       size_hint=(None,None), size = (m_win_x,m_win_y),
                                   )
                part_2 = ComicImage(_index=self._index+1,nocache=False,keep_ratio=False,allow_stretch=True,
                                     id='pi_'+str(self._index)+'b',size_hint = (None,None),size=self.size
                                          )
                scatter.add_widget(part_2)
                part_1.texture = proxyImage.image.texture.get_region(0,0,c_width/2,c_height)
                part_2.texture = proxyImage.image.texture.get_region((c_width/2+1),0,c_width/2,c_height)
                self.texture = part_1.texture
                app.root.ids['comicscreenid'].ids['my_carousel'].add_widget(scatter,self._index+1)
                inner_grid = GridLayout(cols=1, rows =2,id='inner_grid'+str(self._index),size_hint=(None,None),
                                        size=(130,200), spacing=5)
                page_thumb = PageThumbImage(allow_stretch=True,
                                        size=(130,200),size_hint=(None, None),id=str(self._index),_index=self._index)
                page_thumb.texture = part_1.texture
                inner_grid.add_widget(page_thumb)
                page_thumb.parent.bind(pos=app.root.setter('pos'))
                page_thumb.parent.bind(pos=app.root.setter('pos'))
                page_thumb.bind(on_press=app.root.pop.dismiss)
                page_thumb.bind(on_press=page_thumb.click)
                smbutton = Button(size_hint=(None,None),size=(10,10),text='P%sa'%str(self._index+1),text_color=(0,0,0),
                background_color=(1,1,1,.5))

                inner_grid.add_widget(smbutton)
                widget.add_widget(inner_grid)

                inner_grid = GridLayout(cols=1, rows =2,id='inner_grid'+str(self._index+1),size_hint=(None,None),
                                        size=(130,200), spacing=5)
                part_2_thumb = PageThumbImage(allow_stretch=True,
                                        size=(130,200),size_hint=(None, None),id=str(self._index+1),_index=self._index+1)
                part_2_thumb.texture =part_2.texture
                inner_grid.add_widget(part_2_thumb)
                Logger.debug('ok it did it')
                part_2_thumb.parent.bind(pos=app.root.setter('pos'))
                part_2_thumb.parent.bind(pos=app.root.setter('pos'))
                part_2_thumb.bind(on_press=app.root.pop.dismiss)
                part_2_thumb.bind(on_press=part_2_thumb.click)
                smbutton = Button(size_hint=(None,None),size=(10,10),text='P%sb'%str(self._index+1) ,text_color=(0,0,0),
                background_color=(1,1,1,.5))

                inner_grid.add_widget(smbutton)
                widget.add_widget(inner_grid)

            else:
                if proxyImage.image.texture.width > 2*Window.width:
                   self.size_hint=(2,1)
                self.texture = proxyImage.image.texture
                inner_grid = GridLayout(cols=1, rows =2,id='inner_grid'+str(self._index),size_hint=(None,None),
                                        size=(130,200), spacing=5)
                page_thumb = PageThumbImage(source=src_thumb,allow_stretch=True,
                                        size=(130,200),size_hint=(None, None),id=str(self._index),_index=self._index)

                inner_grid.add_widget(page_thumb)
                page_thumb.parent.bind(pos=app.root.setter('pos'))
                page_thumb.parent.bind(pos=app.root.setter('pos'))
                page_thumb.bind(on_press=app.root.pop.dismiss)
                page_thumb.bind(on_press=page_thumb.click)
                smbutton = Button(size_hint=(None,None),size=(10,10),text='P%s'%str(self._index+1),text_color=(0,0,0),
                background_color=(1,1,1,.5))

                inner_grid.add_widget(smbutton)
                widget.add_widget(inner_grid)

    def _abort_download(self, dt):
        '''Stop the image from downloading'''
        Loader.stop()

class MagnifyingGlassScatter(Scatter):
    def __init__(self,**kwargs):
        super(MagnifyingGlassScatter, self).__init__(**kwargs)
        self.mag_glass_x = int(App.get_running_app().config.get('Display', 'mag_glass_size'))
        self.mag_glass_y = int(App.get_running_app().config.get('Display', 'mag_glass_size'))
        self.page_widget = ''
        self.mag_img = ''

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            # do whatever else here
        return super(MagnifyingGlassScatter, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            print 'touch = %s'%str(touch.pos)
            print 'image = %s'%str(self.page_widget.size)
            #get the middle of mag glass
            my_x = self.x + self.mag_glass_x/2
            m_y = self.y + self.mag_glass_y/2
            #self.mag_img.texture = self.page_widget.texture.get_region(my_x,m_y,my_x,my_y)
            self.mag_img.texture = self.page_widget.texture.get_region(my_x,m_y,self.mag_glass_x,self.mag_glass_y)
            # now we only handle moves which we have grabbed
        return super(MagnifyingGlassScatter, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
        return super(MagnifyingGlassScatter, self).on_touch_up(touch)
            # and finish up here

class ComicScreen(Screen):
    def __init__(self,**kwargs):
        self.ab_state = 'closed'
        super(ComicScreen, self).__init__(**kwargs)
        self.move_state = 'open'

    def comicscreen_open_pagescroll_popup(self):
        self.thumb_pop.open()

    def _carousel_call(self):
        my_carousel = App.get_running_app().root.ids['comicscreenid'].ids['my_carousel']

        scatter_w = my_carousel.current_slide

        scatter_w.open_mag_glass()

    def _cal_id(self):
        if self.ab_state == 'closed':
            self.ab_state = 'open'
            c = TopActionBar(id='comicscreenab',)
            self.add_widget(c)
        else:
            for child in self.walk():
                if child.id == 'comicscreenab':
                    my_action_bar = child
            #    print("{} -> {}".format(child, child.id))
            self.ab_state = 'closed'
            self.remove_widget(my_action_bar)



class ComicScatter(Scatter):
    def __init__(self, **kwargs):
        super(ComicScatter, self).__init__(**kwargs)
        self.zoom_state = 'normal'
        self.move_state = 'open'

    def open_mag_glass(self):
        Logger.debug('my id=%s' % str(self.id))

        mag_glass_setting_x = int(App.get_running_app().config.get('Display', 'mag_glass_size'))
        mag_glass_setting_y = int(App.get_running_app().config.get('Display', 'mag_glass_size'))

        comic_image_id = self.id.replace('comic_scatter','pi_')
        print App.get_running_app().root.ids
        try:
            for child in self.walk():
                print child.id
                if child.id == comic_image_id:
                    image_w = child
                    Logger.debug('>>>>>Found grandchild named %s this is the image' %comic_image_id)
                elif child.id == 'mag_glass':
                    mag_glass_w = child
        except:
           Logger.critical('Some bad happened in _call_mag')
        else:
            print 'image_w = %s' % str(image_w)
            if self.move_state == 'open':
                self.move_state = 'locked'
                self.do_scale=False
                self.do_translation=False
                Logger.debug('image_w.center = %d,%d' % (image_w.center_x,image_w.center_y))

                mag_glass = MagnifyingGlassScatter(size=(mag_glass_setting_x,mag_glass_setting_y),size_hint = (None, None),
                                                        do_rotation=False, do_scale=False,
                                                        pos=((image_w.center_x-(mag_glass_setting_x/2)),
                                                             (image_w.center_y-(mag_glass_setting_y/2))
                                                         ),id='mag_glass'
                                                  )
                mag_glass.page_widget = image_w
                mag_glass_image = Image(size_hint= (None,None),pos_hint={'x':1, 'y':1},id='mag_image',keep_ratio=True,
                                        allow_stretch=False,size=mag_glass.size )
                mag_glass.mag_img = mag_glass_image
                mag_glass_image.texture = image_w.texture.get_region(
                                            mag_glass.x,mag_glass.y,mag_glass_setting_x,mag_glass_setting_y)
                mag_glass.add_widget(mag_glass_image)
                self.add_widget(mag_glass)
            else:
                self.move_state = 'open'
                self.do_scale=True
                self.do_translation=True

                self.remove_widget(mag_glass_w)

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