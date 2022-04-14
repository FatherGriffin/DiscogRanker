from threading import Thread
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, CardTransition
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout

from discog import discog

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '600')

class MainGrid(Screen):

    def middle_click(self):
        user = 'griffinbrooks47@gmail.com'
        password = '$Cornelius632'
        t = Thread(target=self.collect_discog(), args=(user, password))
        t.daemon = True
        # start the thread
        t.start()

    def collect_discog(user, password):

        print("collecting discog...")
        d1 = discog(user, password, 'Lil Tecca')  
        d1.spotify_login()
        d1.search()

class DiscogRankerApp(App):
    
    def build(self):

        root = MainGrid()
        return root

DiscogRankerApp().run()
