__version__ = '1.002'
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.image import Image
from settingsjson import settings_json
import urllib2

class RootWidget(FloatLayout):
    '''This the class representing your root widget.
       By default it is inherited from ScreenManager,
       you can use any other layout/widget depending on your usage.
    '''

    manager = ObjectProperty()

    def load_next_page(self, *args):
        base_url = App.get_running_app().config.get('Server', 'url')
        base_file = App.get_running_app().config.get('Server', 'bufferdir')
        carousel = self.ids['my_carousel']
        i = carousel.index
        print carousel.current_slide
        id = 1855
        nextpage = i  + 3
        src = "%s/comic/1855/page/%d" % (base_url, nextpage)
        print 'This is bugger load %s' %src
        response=urllib2.urlopen(src)
        fname='images/%d_P%d.jpg' %(id, i)
        with open(fname,'w') as f:
            f.write(response.read())
        image = Image(source=fname, allow_stretch=True)
        carousel.add_widget(image)

    def load_from_server(self, *args):
        id = 1855
        base_url = App.get_running_app().config.get('Server', 'url')
        carousel = self.ids['my_carousel']
        pagebuffer = int(App.get_running_app().config.get('Server', 'pagebuffer'))
        for i in range(0,pagebuffer+1):
             src = "%s/comic/1855/page/%d" % (base_url, i)
             print src
             response=urllib2.urlopen(src)
             #load images asynchronously
             fname='images/%d_P%d.jpg' %(id, i)
             with open(fname,'w') as f:
                 f.write(response.read())
             image = Image(source=fname, allow_stretch=True)
             carousel.add_widget(image)

        carousel.pos_hit = {'top':1}

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
        return RootWidget()
    def build_config(self, config):
        config.setdefaults('Server',
                {
                'boolexample': True,
                'pagebuffer': 10,
                'optionsexample': 'option2',
                'url': 'http://',
                'bufferdir': self.user_data_dir
                }
            )

    def build_settings(self, settings):
        settings.add_json_panel('Main Settings',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        print config, section, key, value



if __name__ == '__main__':
    CRDroidApp().run()
