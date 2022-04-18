import threading
from tkinter import font

#kivy
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, CardTransition
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty

#kivyMD
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField 

#spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import time
import requests
from discog import discog

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '600')

class MainGrid(Screen, threading.Thread):
    
    def __init__(self, **kwargs):
        super(MainGrid, self).__init__(**kwargs)
        
        # used so only one thread is executed at a time for the artist search button
        self.mid_button_bool = True
        
        # discography will in a separate function
        self.d1 = None
        
        self.artist = ''
        self.artist_urm = ''
        
        self.cid = '9f9c28b122a1448f817b7a2e7a3ddb71'
        self.secret = '5f0ec05e3ec84dcb86b9e7f8650caaea'
        
        self.ids.console_log.text = ''
        
        #search bar - text input
        self.artist_search = TextInput(
            size_hint=(0.89,1),
            font_name='Fonts\Lato-Light.ttf',
            font_size=55,
            foreground_color=(193/255, 192/255, 200/255, 1),
            padding_x= [10,1],
            background_color=(0,0,0,0),
            cursor_color=(193/255, 192/255, 200/255, 1),
            cursor_width=1.5,
            hint_text='Enter Artist Name',
            hint_text_color=(193/255, 192/255, 200/255, 1),
            
            multiline=False,
            on_text_validate=self.submit_search
        )
        self.ids.artist_search_bar.add_widget(self.artist_search)
        
        #search bar - search button
        self.artist_search_button = Button(
            size_hint=(0.11, 1),
            text='search',
            opacity=0,
            on_press=self.submit_search,
        )
        self.ids.artist_search_bar.add_widget(self.artist_search_button)
        
        #button to switch layouts to ranking screen
        self.rank_songs_button = Button(
            size_hint=(0.1, 0.05),
            color=(193/255, 192/255, 200/255, 1),
            pos_hint={'center_x': 0.746, 'top': 0.93}, 
            text='Rank ->',     
            on_release=(self.begin_rank), 
        )
        self.ids.bottom_section.add_widget(self.rank_songs_button)
        
    def submit_search(self, touch=None):
    
        if self.mid_button_bool:
        
            self.artist = self.artist_search.text
            
            self.artist_search.hint_text = self.artist_search.text
            self.artist_search.text = ''
            
            self.mid_button_bool = False
            threading.Thread(target=self.pull_discog, daemon=True).start()
            self.ids.console_log.text = 'Searching for artist...'
            print("Searching for artist...")
        
    def pull_discog(self):
        
        self.d1 = discog(self.artist)
        self.artist_urm = self.d1.pull_catalogue()
        spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id='9f9c28b122a1448f817b7a2e7a3ddb71', client_secret='5f0ec05e3ec84dcb86b9e7f8650caaea')
        )
            
        album_data = spotify.artist_albums(self.artist_urm, album_type='album') 
        albums = album_data['items']
        
        
        #loop stores last album instance here - Spotipy sends duplicates so this loop filters them out
        #Loop stores album data in Discog class object "d1" - album names, album codes, and covers
        temp_name = ''
        for i, album in enumerate(albums):
            
            t, u, c = album['name'],album['uri'],album['images'][0]['url']
            
            if album['name'] != temp_name:
                self.d1.add_album(
                    title=t, 
                    uri=u,  
                    cover=c
                )
                temp_name = album['name']   
        
        #loop generates tracklist for each album - stores data in d1 tracklist variable
        for i in range(len(self.d1.albums)):
            
            c = self.d1.albums[i]
            tracks = []
            
            track_data = spotify.album_tracks(album_id=self.d1.album_uris[i])
            track_list = track_data['items']
            
            for song in track_list:
                tracks.append(song['name'])
            
            self.d1.add_tracklist(c, tracks)
            
            
        time.sleep(1)
        #re-enables artist search button
        self.mid_button_bool = True
        self.ids.console_log.text = 'Discography generated!'

    def begin_rank(self, touch=None):
        
        if self.mid_button_bool and self.d1:
            print('Switching screens to begin ranking!')
            self.manager.current = 'rank'

class Ranker_Screen(Screen):
    
    def __init__(self, **kwargs):
        super(Ranker_Screen, self).__init__(**kwargs)
        pass



class DiscogRankerApp(App):
    
    def build(self):

        root = ScreenManager()
        root.add_widget(MainGrid(name='main'))
        root.add_widget(Ranker_Screen(name='rank'))

        return root

if __name__ == "__main__":
    app = DiscogRankerApp()
    app.run()


