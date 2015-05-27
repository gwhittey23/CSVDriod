__version__ = '1.004'
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
from kivy.uix.image import Image
from settingsjson import settings_json
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty
from csvdb.csvdroid_db import build_db
from kivy.logger import Logger
from csconnector import ComicStream, CsComic
import os.path
import urllib2

class ComicScreenBntListItem(Button):
    id = StringProperty('')
    image = StringProperty('')
    title = StringProperty('')
    label = StringProperty('')
    pass

    def click(button):
        app = App.get_running_app()
        app.root.manager.current = 'comicscreen'
        app.root.ids['my_carousel'].index = int(button.id)

class LibScreenBntListItem(Button):
    id = StringProperty('')
    image = StringProperty('')
    title = StringProperty('')
    label = StringProperty('')
    pass

    def click(button):
        app = App.get_running_app()
        app.root.manager.current = 'comicscreen'
        print button.id
        app.root.load_comic_screen(int(button.id))



class ButtonList(GridLayout):
    pass

class RootWidget(FloatLayout):

    manager = ObjectProperty()

    def load_lib_screen(self, *args):
        display_mode = 'Series' #default mode


        id = 96
        page_count = 22
        base_url = App.get_running_app().config.get('Server', 'url')
        base_file = App.get_running_app().config.get('Server', 'storagedir')
        grid = GridLayout(cols=3, size_hint=(None,None),spacing=10,padding=10, pos_hint = {.2,.2})
        grid.bind(minimum_height=grid.setter('height'))

        for i in range(0,page_count):
            fname='%s/%d_P%d.jpg' %(base_file, id, i)
            if  os.path.isfile(fname) == False:
                 src = "%s/comic/%d/page/%d" % (base_url, id, i)
                 print src
                 print 'getting cache copy %s from %s' % (fname, src)
                 response=urllib2.urlopen(src)
                 #load images asynchronously
                 with open(fname,'w') as f:
                     f.write(response.read())
            page_button = LibScreenBntListItem(id=str(96), text='#Page' + str(i), size=(129, 200), size_hint=(None, None),
                                         image=base_file + '/' + str(id) + '_P' + str(i) + '.jpg',
                                         )
            grid.add_widget(page_button)
        scroll = ScrollView( size_hint=(.9,.85), do_scroll_y=True, do_scroll_x=False,
                             pos_hint={'center_x': .6, 'center_y': .5} )
        scroll.add_widget(grid)
        self.ids['fl1'].add_widget(scroll)


    def load_comic_screen(self, comicstream_number):
        Logger.debug(str(comicstream_number))

        cscomic = CsComic(comicstream_number)
        base_url = App.get_running_app().config.get('Server', 'url')
        base_file = App.get_running_app().config.get('Server', 'storagedir')
        carousel = self.ids['my_carousel']
        grid = GridLayout(rows=1, size_hint=(None,None),spacing=10,padding=10)
        grid.bind(minimum_width=grid.setter('width'))
        for i in range(0, cscomic.page_count):
            fname='%s/%d_P%d.jpg' %(base_file, comicstream_number, i)
            if  os.path.isfile(fname) == False:
                src = "%s/comic/%d/page/%d" % (base_url, comicstream_number, i)
                Logger.info('Getting Server info for %s' % comicstream_number)
                response=urllib2.urlopen(src)
                #load images asynchronously
                with open(fname,'w') as f:
                    f.write(response.read())
            page_button = ComicScreenBntListItem(
                            id=str(i), text='#Page' + str(i),
                            size=(129, 200), size_hint=(None, None),
                            image=base_file + '/' + str(comicstream_number) + '_P' + str(i) + '.jpg',)
            grid.add_widget(page_button)
            image = Image(source=fname, allow_stretch=True)
            print carousel.index
            carousel.add_widget(image)
        carousel.pos_hit = {'top':1}

        #Build the popup scroll of page buttons
        scroll = ScrollView( size_hint=(1,1), do_scroll_x=True, do_scroll_y=False )
        scroll.add_widget(grid)
        self.pop = Popup(title='Pages', content=scroll, pos_hint ={'y': .0001},size_hint = (1,.23))

    def open_pagescroll_popup(self):
        self.pop.open()

class ComicScreen(Screen):
    pass

class SecondScreen(Screen):
    pass

class CRDroidApp(App):

    '''This is the main class of your app.
       Define any app wide entities here.
       This class can be accessed anywhere inside the kivy app as,
       in python::

         app = App.get_running_app()
         print (app.title)

       in kv language::

         on_release: print(app.title)
       Name of the .kv file that is auto-loaded is derived from the name
       of this class::

         MainApp = main.kv
         MainClass = mainclass.kv

       The App part is auto removed and the whole name is lowercased.
    '''
    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = True
        print 'user_data_dir = %s' %self.user_data_dir
        # setting = self.config.get('example', 'url')
        # print setting
        if  os.path.isfile('cachedb.sqlite') == False:
            build_db()
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

    def build_settings(self, settings):
        settings.add_json_panel('Main Settings',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        print config, section, key, value

    def get_full_data(self):
        comicstrem =ComicStream()
        Logger.debug('getting full data')
        comic_list = comicstrem.get_fulldata()

if __name__ == '__main__':
    CRDroidApp().run()
