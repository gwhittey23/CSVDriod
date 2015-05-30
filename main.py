__version__ = '1.220007'
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

    manager = ObjectProperty()

    def load_lib_screen(self, *args):

        print self.ids.mywid.ids['my_carousel']


        display_mode = 'Series' #default mode
        id = 96
        # page_count = 22
        # base_url = App.get_running_app().config.get('Server', 'url')
        # base_file = App.get_running_app().config.get('Server', 'storagedir')
        # grid = GridLayout(cols=4, size_hint=(None,None),spacing=(10,50),padding=10, pos_hint = {.5,.2})
        # grid.bind(minimum_height=grid.setter('height'))
        #
        # for i in range(0,page_count):
        #     fname='%s/%d_P%d.jpg' %(base_file, id, i)
        #     src = "%s/comic/%d/page/%d" % (base_url, id, i)
        #     if  os.path.isfile(fname) == False:
        #
        #         try:
        #             r = requests.get(src)
        #             r.raise_for_status()
        #         except HTTPError:
        #             Logger.critical('HTTPerror for %s' % src )
        #         else:
        #         #load images asynchronously
        #            with open(fname,'w') as f:
        #                  f.write(r.content)
        #
        #     inner_grid = GridLayout(cols=1, rows =2,id='inner_grid'+str(i),size_hint=(None,None),size=(130,200),spacing=5)
        #     # page_button = LibScreenBntListItem(id=str(96), text='#Page' + str(i), size=(129, 200), size_hint=(None, None),
        #     #                              image=base_file + '/' + str(id) + '_P' + str(i) + '.jpg',
        #     #
        #     #                              )
        #     page_button = ComicScreenBntListItem(source=src, size=(129, 200), size_hint=(None, None),)
        #
        #     inner_grid.add_widget(page_button)
        #     smbutton = Button(size_hint=(None,None),size=(10,10),text='P%s'%str(i+1),background_color=(0,0,0,0))
        #     inner_grid.add_widget(smbutton)
        #     grid.add_widget(inner_grid)
        #
        #
        # scroll = ScrollView( size_hint=(.95,.85), do_scroll_y=True, do_scroll_x=False,
        #                      pos_hint={'center_x': .5, 'center_y': .5} )
        # scroll.add_widget(grid)
        # self.ids['fl1'].add_widget(scroll)



    def load_comic_screen(self, comicstream_number):
        carousel = self.ids.comicscreenid.ids['my_carousel']
        carousel.clear_widgets()

        Logger.debug(str(comicstream_number))
        page_count = 22
        comicstream_number = int(self.ids['txt1'].text)
        id = '96'
       # cscomic = CsComic(comicstream_number)
        base_url = App.get_running_app().config.get('Server', 'url')
        base_dir = 'images'
        #base_file = App.get_running_app().config.get('Server', 'storagedir')
        scroll = ScrollView( size_hint=(1,1), do_scroll_x=True, do_scroll_y=False )
        self.pop = Popup(id='page_pop',title='Pages', content=scroll, pos_hint ={'y': .0001},size_hint = (1,.33))
        grid = GridLayout(rows=1, size_hint=(None,None),spacing=5,padding_horizontal=5,id='outtergrd')
        grid.bind(minimum_width=grid.setter('width'))
        for i in range(0, page_count):
            comic_dir = '%s/%s' %(base_dir, comicstream_number)
            if not os.path.exists(comic_dir):
                os.makedirs(comic_dir)
            fname='%s/%d/%d_P%d.jpg' %(base_dir, comicstream_number, comicstream_number, i)
            src_full = "%s/comic/%d/page/%d?max_height=1200#.jpg" % (base_url, comicstream_number, i)
            src_thumb = "%s/comic/%d/page/%d?max_height=200#.jpg" % (base_url, comicstream_number, i)
            image = ComicImage(source=src_full,nocache=False,keep_ratio=False,allow_stretch=True)
            print image._coreimage.size
            #expermenatal adding in saving to cache need to implement option turn saving pages on/off
            #image._coreimage.bind(on_load=self.on_image_loaded)
            scatter = ComicScatter(do_rotation=False,id='sclay'+str(i),scale_min=1, scale_max=2)
            scatter.add_widget(image)
            carousel.add_widget(scatter)
            scatter.parent.bind(pos=self.setter('pos'))
            scatter.parent.bind(size=self.setter('size'))
            # next block code is for making the scrolling page_thumb popup.
            inner_grid = GridLayout(cols=1, rows =2,id='inner_grid'+str(i),size_hint=(None,None),size=(130,200),
                                    spacing=5)
            page_image = PageImage(source=src_thumb,allow_stretch=True,
            size=(130,200),size_hint=(None, None),id=str(i))

            inner_grid.add_widget(page_image)
            page_image.parent.bind(pos=self.setter('pos'))
            page_image.parent.bind(pos=self.setter('pos'))
            page_image.bind(on_press=self.pop.dismiss)
            page_image.bind(on_press=page_image.click)
            smbutton = Button(size_hint=(None,None),size=(10,10),text='P%s'%str(i+1),text_color=(0,0,0),
            background_color=(1,1,1,.5))

            inner_grid.add_widget(smbutton)
            grid.add_widget(inner_grid)


        #Build the popup scroll of page buttons

        scroll.add_widget(grid)

        #content.bind(on_press=popup.dismiss)
    def comicscreen_open_pagescroll_popup(self):
        self.pop.open()
    #going to add in save to disc after asyncimage if done downloading.
    # def on_image_loaded(self, *args):
    #     pass

    def zoom_me(self):
        '''Zoom in or back to normal this is disabled atm


        :return:
        '''
        carousel = self.ids['my_carousel']
        print carousel.current_slide.zoom_state
        # carousel.current_slide.scale = 1.5
        mat = Matrix().scale(1.5, 1.5, 1.5)
        carousel.current_slide.apply_transform(mat,anchor=(50,50))
    def my_load_next(self):
        app = App.get_running_app()
        app.root.manager.current = 'comicscreen'





class CRDroidApp(App):


    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = True
        print 'user_data_dir = %s' %self.user_data_dir
        # setting = self.config.get('example', 'url')
        # print setting
        # if  os.path.isfile('cachedb.sqlite') == False:
        #    # build_db()

        return RootWidget()
    def build_config(self, config):
        config.setdefaults('Server',
                {
                'boolexample': True,
                'pagebuffer': 10,
                'optionsexample': 'option2',
                'url': 'http://',
                'storagedir': self.user_data_dir
                }
            )
        Factory.register('ComicScreen', cls=ComicScreen)
    def build_settings(self, settings):
        settings.add_json_panel('Main Settings',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        print config, section, key, value

    def get_full_data(self):
        # comicstrem =ComicStream()
        Logger.debug('getting full data')
        # comic_list = comicstrem.get_fulldata()

if __name__ == '__main__':
    CRDroidApp().run()
