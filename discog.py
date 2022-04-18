import time
from typing import KeysView
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import threading

class discog:
    
    def __init__(self, artist):
        
        self.artist = artist
        self.artist_keyword = '' + artist + ' spotify'
        self.artist_urn = None
        
        self.albums = []
        self.album_uris = []
        self.track_list = {}
        self.album_covers = []

        self.PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.s = Service(self.PATH)
        
        self.artist_keyword = self.artist_keyword.replace(' ', '+')

    def pull_catalogue(self):
        
            #instantiates window & pulls up Spotify
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
            #runs selenium in the background / delete this line to make a physical window appear
        self.options.add_argument("headless")
        
        self.driver = webdriver.Chrome(service=self.s, options=self.options)
        #self.driver.maximize_window()
        
        for i in range (1):
            self.driver.get("https://www.google.com/search?q=" + self.artist_keyword + '&start' + str(i))
        
        time.sleep(1)
        
        xp1 = '//a[@href]'
        self.hyperlinks = self.driver.find_elements_by_xpath(xp1)
        
        
        for link in self.hyperlinks:

            if link.get_attribute("href")[0:31] == 'https://open.spotify.com/artist':
                self.artist_urn = link.get_attribute("href").replace(
                    'https://open.spotify.com/artist/', ''
                    )
                break
        
        self.driver.close()
        
        return self.artist_urn
    
    def add_album(self, title, uri, cover):
        self.albums.append(title)
        self.album_uris.append(uri)
        self.album_covers.append(cover)
    
    def add_tracklist(self, title, tracklist):
        self.track_list.update({title: tracklist})


#artist_name = input("\nWhat artist discography do you want to use? ")
#print("\nYou entered: " + artist_name)

#instantiates user specified discography
#d1 = discog(user, password, 'Lil Tecca')  
#d1.spotify_login()
#d1.search()

