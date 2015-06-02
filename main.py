__version__ = '1.220012'
DEBUG = True
import kivy
kivy.require('1.8.0')
if DEBUG:
    from kivy.config import Config
    print 'setting windows size'
    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '1024')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.settings import SettingsWithSidebar
from settingsjson import settings_json,settings_json_dispaly
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from screens.comic_screen import ComicScreen, ComicScatter, PageThumbImage, ComicImage
from screens.library_screen import LibraryScreen
from kivy.uix.actionbar import ActionBar
from kivy.properties import ObjectProperty
#from csvdb.csvdroid_db import build_db
from kivy.logger import Logger
from kivy.loader import Loader
from kivy.lang import Factory
from kivy.core.window import Window
from functools import partial
from kivy.graphics.transformation import Matrix


class RootWidget(FloatLayout):

    manager = ObjectProperty()

    def load_lib_screen(self, *args):
        display_mode = 'Series' #default mode




        # base_url = App.get_running_app().config.get('Server', 'url')
        # def got_data(req,reults):
        #     print reults
        #     #comic = CsComic(reults)
        #
        #
        # if display_mode == 'Series':
        #    #get Series list
        #     src = "%s/entities/series" % (base_url)
        #     Logger.debug('getting series list')
        #
        #     Logger.debug(src)
        #     req= UrlRequest(src,got_data)
        #
        # id = 96
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
        #     lib_page_button = ComicScreenBntListItem(source=src, size=(129, 200), size_hint=(None, None),)
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
        m_win_x = Window.width
        m_win_y = Window.height
        carousel = self.ids.comicscreenid.ids['my_carousel']
        carousel.clear_widgets()

        Logger.debug(str(comicstream_number))
        page_count = 22
        comicstream_number = int(self.ids['txt1'].text)
        id = '96'
       # cscomic = CsComic(comicstream_number)
        base_url = App.get_running_app().config.get('Server', 'url')
        base_dir = 'comic_page_images'
        scroll = ScrollView( size_hint=(1,1), do_scroll_x=True, do_scroll_y=False,id='page_thumb_scroll')
        self.pop = Popup(id='page_pop',title='Pages', content=scroll, pos_hint ={'y': .0001},size_hint = (1,.33))
        grid = GridLayout(rows=1, size_hint=(None,None),spacing=5,padding_horizontal=5,id='outtergrd')
        grid.bind(minimum_width=grid.setter('width'))
        for i in range(0, page_count):

            src_full = "%s/comic/%d/page/%d?max_height=1200#.jpg" % (base_url, comicstream_number, i)
            src_thumb = "%s/comic/%d/page/%d?max_height=200#.jpg" % (base_url, comicstream_number, i)

            comic_page_image = ComicImage(src=src_full, _index=i,nocache=False,keep_ratio=False,allow_stretch=True,id='pi_'+str(i),
                                          size_hint = (None,None),size=self.size
                                          )
            proxyImage = Loader.image(src_full)

            scatter = ComicScatter(do_rotation=False, do_scale=False,do_translation_x=False,id='comic_scatter'+str(i),
                                   scale_min=1, scale_max=2, size_hint=(None,None), size = (m_win_x,m_win_y),


                                   )
            scatter.add_widget(comic_page_image)
            carousel.add_widget(scatter)
            c_index =  len(carousel.slides)
            comic_page_image.car_index = c_index

            scatter.parent.bind(pos=self.setter('pos'))
            scatter.parent.bind(size=self.setter('size'))
            proxyImage.bind(on_load=partial(comic_page_image._image_downloaded, grid,comicstream_number))


        #Build the popup scroll of page buttons

        scroll.add_widget(grid)

        #content.bind(on_press=popup.dismiss)
    def comicscreen_open_pagescroll_popup(self):
        self.pop.open()
        app = App.get_running_app()



class TopActionBar(ActionBar):
    print 'ok'




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
                'url': 'http://',
                'storagedir': self.user_data_dir
                })



        Factory.register('ComicScreen', cls=ComicScreen)
    def build_settings(self, settings):
        settings.add_json_panel('Server Settings',
                                self.config,
                                data=settings_json)
        settings.add_json_panel('Display Settings',
                                self.config,
                                data=settings_json_dispaly)

    def on_config_change(self, config, section,
                         key, value):
        print config, section, key, value

    def get_full_data(self):
        # comicstrem =ComicStream()
        Logger.debug('getting full data')
        # comic_list = comicstrem.get_fulldata()
    def on_pause(self):
      # Here you can save data if needed
         return True

    def on_resume(self):
      # Here you can check if any data needs replacing (usually nothing)
        pass

if __name__ == '__main__':
    CRDroidApp().run()
