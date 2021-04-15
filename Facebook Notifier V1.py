# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import time
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import random
import bs4
import datetime as dt
from sendemail import *

class Facebook:

    def __init__(self):
        
        self.send=[]
        self.base_url = "https://www.facebook.com/marketplace/114751268540391/electronics"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.extracted=[]
        
        options = Options()
        ua = UserAgent()
        options = Options()
        options.headless = False
        #ua = UserAgent()
        userAgent = ua.firefox

        options.add_argument('--no-sandbox')
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--proxy-server="direct://"')
        options.add_argument('--proxy-bypass-list=*')


        options.add_argument("--disable-dev-shm-usage")
        #driver = webdriver.Chrome(chrome_options=options)
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(30)
        #self.logged_in =False
        self.five_hundred_miles =False


    def navigate_to_facebook(self):
        
        driver = self.driver
        driver.get("https://www.facebook.com/marketplace/portland/rv-campers?carType=rv_camper&sortBy=creation_time_descend")
        
    def return_bs4(self):
        source_page = self.driver.page_source
        c=bs4.BeautifulSoup(source_page,'html.parser')

        return c

    def select_500_km_radius(self):
        #click_radius and select the radius drop down
        
        radio = self.return_bs4()
        self.driver.find_element_by_xpath('//*[@id="seo_filters"]/div[1]').click()
        time.sleep(2)
        radio = self.return_bs4()
        check_radius = True
        while check_radius:
            try:
                radio = self.return_bs4()
                d=radio.find_all('label',{'aria-label':'Radius'})
                label_id = d[0].attrs['for']
                check_radius =False
            except:
                time.sleep(1)
        
        self.driver.find_element_by_id(label_id).click()
        #time.sleep(2)
        
        check_miles =True
        while check_miles:
            try:
                radio = self.return_bs4()
                five_hundred=radio.find_all('div',{'role':'menuitemradio'})[10].attrs['class'][0]
                check_miles= False
            except:
                time.sleep(1)
            
        drop_down_500 =''
        
        for i in self.driver.find_elements_by_class_name(five_hundred):
            if '500 kilometres' in i.text:
                drop_down_500=i
                print("Found")
        print(drop_down_500)
        drop_down_500.click()
        #apply
        apply_class=radio.find_all('div',{'aria-label':'Apply'})[0].attrs['class'][0]
        apply_button=''
        
        for i in self.driver.find_elements_by_class_name('oajrlxb2'):
            if 'Apply' in i.text:
                apply_button=i
                
        apply_button.click()

        self.five_hundred_miles = True

    def extract_details(self):
        v=a.return_bs4()
        h=v.find_all('a')
        found = []
        for i in h:
            if '/marketplace/item/' in i['href']:
                print('Scanning for new items')
                price = i.find_all('span')[1].text
                link = 'https://facebook.com'+i['href']
                name = i.find_all('img')[0].attrs['alt']
                image = i.find_all('img')[0]['src']
                
                found.append([name,price,link,image])
        return found
    
    def main(self):
        
        self.navigate_to_facebook()
        self.select_500_km_radius()
        start = dt.datetime.now()
        wait_time = 40
        
        while True:
            try:
                now = dt.datetime.now()
                v= now-start
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                if v.seconds >=wait_time:
                    
                    self.driver.refresh()
                    self.select_500_km_radius()
                    extracted = self.extract_details()
                    wait_time = random.randint(40,60)
                    start = dt.datetime.now()
                    to_send = []
                    for i in extracted:
                        
                        if i in self.extracted:
                            pass
                        else:
                            print('Found New AD')
                            print(i[0])
                            print(i[1])
                            print(i[2])
                            print(i[3])
                            print('************')
                            to_send.append(i)
                            self.send.append(i)
                            
                        if len(to_send) > 5:
                            break
                    
                    for i in extracted:
                        self.extracted.append(i)
                    

                else:
                    time.sleep(1)
                self.send_alerts()
                
            except Exception as e:
                print(e)
                
    def send_alerts(self):
        
        if len(self.send)==1:
            #send one
            text = "A New Facebook AD Has Been Posted \n\nPrice : {} \n\n"+"Link: {}"
            found=[]

            
            for i in self.send:
                print('sending email')
                trigger(i[0],text.format(i[1],i[2]))
                open('sent.txt','a').write(str(i[0]))
                open('sent.txt','a').write('\n')
                
        elif len(self.send)>1:
            print('sending emails')
            text = "New Facebook ADS Posted \n\n"
            things='Price : {} \n\n"+"Link: {}\n\n'
            #all
            oul = ''
            for i in self.send:
                oul+=things.format(i[1],i[2])
                
            trigger(text,oul)
            for i in self.send:
                open('sent.txt','a').write(str(i[0]))
                open('sent.txt','a').write('\n')
            
            #[name,price,link,image]
        else:
            pass
            
        self.send = []


a=Facebook()
a.main()
            
