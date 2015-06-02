from kivy.app import App
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout

Builder.load_string('''
<MyScreen>:

    padding: 20
    canvas.before:
        Color:
            rgb: .6, .6, .6
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'graphics/Wood_floor_by_gnrbishop.jpg'


''')

class MyScreen(GridLayout):
    pass
class Mybutton(ButtonBehavior,Image):
    pass
class MyApp(App):

    def build(self):
        root = MyScreen()
        for i in range(25):
            btn = Mybutton(text=str(i), width=130, height=200, size_hint=(None, None),
                           pos = self.pos
                         ,background_normal = StringProperty('graphics/Top-view-book-mockup/top view2.jpg')
                         )
            root.add_widget(btn)

        return root
if __name__ == '__main__':
    MyApp().run()
