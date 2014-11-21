import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import random
      
import urllib2
import re

class ScrapeImg:
    """Scrapes a website for images, configurable for different sizes or types."""
        
    ID = 'ScrapeImg'
    # list of unknown images, need more analysis.
    u_img = []    

    
    def __init__(self, url, webdriver):
        self.start_url = url
        self.br = webdriver
        self.br.set_page_load_timeout(3)                        
        self.navigate(url)
        
    def down_img(self, src):




        if src == None:
            return False
        if not "http" in src:
            return False
                            
        #print 'SRC: '+src     
        
        #works only in python 2.7
        #download image.
        image_type = "unknown"

        if ".png" in src:
            image_type = "png"
        if ".gif" in src:
                    image_type = "gif"
        if ".jpeg" in src or ".jpg" in src:
            image_type = "jpg"
        if image_type in "unknown":
            # add to unknown images
            self.u_img.append(src)
            return False
                        

        try:
            response = urllib2.urlopen(src)
            #print 'Downloading image: '+src               
        except:
            return False
        img_data = response.read()    
        size = len(img_data)
        print 'Size: {}'.format(size)
        
        #image name
        filename = src.rsplit('/',1)[1]
        randi = random.randint(1, 10000)  
        if size > 150:
            newFile = open ("img/"+filename+"{}_.".format(randi)+image_type, "wb")
            newFileByteArray = bytearray(img_data)
            newFile.write(newFileByteArray)    
            
        return False
            

    def navigate(self, url):
        try:
            print 'Navigating to '+url
            self.br.get(url)
            return True
        except:
            print "Page timed out or something else happened"
            return False        
        
        

