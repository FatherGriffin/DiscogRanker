import time
from typing import KeysView
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import threading

class discog:
    
    def __init__(self, s_user, s_pass, artist):

        self.var = 1
        self.user = s_user
        self.password = s_pass
        self.artist = artist

        self.PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.s = Service(self.PATH)

    def spotify_login(self):
        
            #instantiates window & pulls up Spotify
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
            #runs selenium in the background / delete this line to make a physical window appear
        #self.options.add_argument("headless")
        
        self.driver = webdriver.Chrome(service=self.s, options=self.options)
        #self.driver.maximize_window()
        self.driver.get("https://accounts.spotify.com/en/login")

            #enters user
        xp1 = '//*[@id="login-username"]'
        self.login_user = self.driver.find_elements_by_xpath(xp1)[0]
        self.login_user.send_keys(self.user)
            #enters password
        xp2 = '//*[@id="login-password"]'
        self.login_pass = self.driver.find_elements_by_xpath(xp2)[0]
        self.login_pass.send_keys(self.password)
            #click login button
        xp3 = '//*[@id="login-button"]'
        self.login_click = self.driver.find_elements_by_xpath(xp3)[0]
        self.login_click.click()
        
        print('Successful Login')
        time.sleep(0.5)
        
            #redirects to spotify website
        xp4 = '/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/button[2]'
        self.login_click = self.driver.find_elements_by_xpath(xp4)[0]
        self.login_click.click()

        print('redirected to web player')
        
    def search(self):

            #brings up search bar
        self.driver.get("https://open.spotify.com/search")
        
        time.sleep(2)
        
            #types in artist name
        xp5 = '//*[@id="main"]/div/div[2]/div[1]/header/div[3]/div/div/form/input'
        self.artist_search = self.driver.find_element_by_xpath(xp5)
        self.artist_search.send_keys(self.artist)

        print('artist name typed')
        
        time.sleep(1)
        
            #brings up artist profile
        xp6 = '//*[@id="searchPage"]/div/div/section[1]/div[2]'
        self.albums = self.driver.find_element_by_xpath(xp6)
        self.albums.click()

        print('artist profile located')
        
        time.sleep(2)
        
            #brings up artist discography
        xp7 = '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div/div[2]/div[3]/section[2]/div[1]/div/a'
        self.albums_hyperlink = self.driver.find_element_by_xpath(xp7).get_attribute("href")
        self.driver.get(self.albums_hyperlink)

        print('finished!')
        
        self.driver.close()
    

user = 'griffinbrooks47@gmail.com'
password = '$Cornelius632'

#artist_name = input("\nWhat artist discography do you want to use? ")
#print("\nYou entered: " + artist_name)

#instantiates user specified discography
#d1 = discog(user, password, 'Lil Tecca')  
#d1.spotify_login()
#d1.search()

