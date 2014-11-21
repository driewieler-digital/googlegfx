from DDZip import DDZip
from ScrapeImg import ScrapeImg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import time

import urlparse

class ScrapeImgGoogle(ScrapeImg):

    def zip_images(self):
        archiver = DDZip()
        archiver.write_zip("img/*", "archives/images.zip", True)
        archiver.print_zip("archives/images.zip")
        
    def get_images(self):
    #<div class="hdtb_mitem hdtb_msel hdtb_imb">Images</div>
        driver = self.br
        WebDriverWait(driver, 30).until( EC.presence_of_element_located((By.CLASS_NAME, "hdtb_mitem")) )                                           
        btns = driver.find_elements_by_class_name("hdtb_mitem")
        
        images_btn = None
        found = False
        for b in btns:
            if "Images" in b.text or "Afbeeldingen" in b.text:
                images_btn = b
                found = True
                break
        if not found:
            print 'No images button found.'
            return False
            
        href = images_btn.find_element_by_tag_name("a").get_attribute("href")
        # go to the images page
        self.navigate(href)
        
        WebDriverWait(driver, 30).until( EC.presence_of_element_located((By.CLASS_NAME, "rg_l")) )                                                   
        img_btns = driver.find_elements_by_class_name("rg_l")            
        
        img_btns[0].click()
#<a data-href="http://upload.wikimedia.org/wikipedia/commons/3/38/Flamingos_Laguna_Colorada.jpg" data-ved="0CAQQjBw" href="http://upload.wikimedia.org/wikipedia/commons/3/38/Flamingos_Laguna_Colorada.jpg" class="irc_fsl irc_but"><span class="irc_but_t">Afbeelding bekijken</span></a>        
#irc_but_t
        time.sleep(2)
        WebDriverWait(driver, 30).until( EC.presence_of_element_located((By.CLASS_NAME, "irc_fsl")) )                                                   
        links = driver.find_elements_by_tag_name("a")            
        
        c=0
        for l in links:
        
            if c > 5:
                print 'Max reached'
                return True
            try:
                h1 = l.get_attribute("href")          
                if self.a_has_image(h1):
                    #print 'Link found: '+h1     
                    
                    url = h1
                    par = urlparse.parse_qs(urlparse.urlparse(url).query)
                    img_url = par['imgurl'][0]

                    #print "Image URL: {}".format(img_url)                     
                    self.down_img(img_url)
                    c += 1
                       
            except:
                continue
        
        return True
        # get first 10 image links
        
    def a_has_image(self, href):
        if "png" in href:
            return True
        if "jpg" in href:
            return True
        if "jpeg" in href:
            return True
        if "gif" in href:
            return True
        return False
        
        
    
        
# commands
mode = 'online'
#mode = 'offline'

print 'Mode: '+mode

if mode == 'online':

    # set the profile for the webdriver.
    profile = webdriver.FirefoxProfile()
    profile.set_preference("permissions.default.image", 2);            
    profile.set_preference("general.useragent.override","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.24 (KHTML, like Gecko) Chrome/26.0.1374.0 Safari/537.24")        
    
    #set the driver
    
    #dcap = dict(DesiredCapabilities.PHANTOMJS)
    #dcap["phantomjs.page.settings.userAgent"] = (
    #    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
    #    "(KHTML, like Gecko) Chrome/15.0.87"
    #)
    #dcap["phantomjs.page.settings.resourceTimeout"] =( '500000')

    #driver = webdriver.PhantomJS(desired_capabilities=dcap)    
    
    driver = webdriver.Firefox(profile)    

    # start up scrapers, and tell them to log in.
    #url = "https://www.google.com/search?q=fountain+photos&tbm=isch"
    #url = "https://www.google.com/"
    #url = "http://www.microsoft.com"
    #url = "http://www.xkcd.com"
    
    
    
    url = "https://www.google.nl/#q="
    search = raw_input('Search: ')            
    if len(search) < 2:
        print 'Not a valid term'
        quit()
    url = url + search
    
    scraper = ScrapeImgGoogle(url, driver)
    r = scraper.get_images()
    if r:
        print 'Zipping.'
        scraper.zip_images()

    raw_input("Any key to quit.")

    driver.quit()        
    
        