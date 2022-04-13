import time
from typing import KeysView
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class discog:
    
    def __init__(self, s_user, s_pass, artist=''):

        self.var = 1
        self.user = s_user
        self.password = s_pass
        self.artist = artist

        self.PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.s = Service(self.PATH)

    def search(self):
        
            #instantiates window & pulls up Spotify
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=self.s, options=self.options)
        self.driver.maximize_window()
        self.driver.get("https://accounts.spotify.com/en/login")

            #enters login information
        xp = '//*[@id="login-username"]'
        self.login_button = self.driver.find_elements_by_xpath(xp)[0]
        self.login_button.send_keys(self.user)
    
    def close_window(self):

            #terminates chrome window
        self.driver.close()
        

#PATH = "C:\Program Files (x86)\chromedriver.exe"
#s = Service(PATH)

#options = webdriver.ChromeOptions()
#options.add_experimental_option('excludeSwitches', ['enable-logging'])
#driver = webdriver.Chrome(service=s, options=options)

#driver.maximize_window()

#driver.get("https://www.spotify.com/us/")


