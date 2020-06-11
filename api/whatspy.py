from selenium import webdriver
from datetime import datetime
from time import sleep

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException



# from chromepy.chrome import Chrome
from chromepy.remote import ChromeRemote


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Whatsapp(metaclass=Singleton):
    
    def __init__(self):
        self.selectors = {
            'qrcode': 'canvas',
            'search_input':  '#side .copyable-text.selectable-text',
            'search_result': '#side span[title="{}"]',
            'message_input': '#main footer div.copyable-text.selectable-text',
            'message_send':  '#main footer button span[data-icon="send"]'
        }
        
        url = 'http://web.whatsapp.com'
        
        self.chrome = ChromeRemote()
        
        if self.chrome.current_url != url:
            self.chrome.get(url)
        
    def _wait_for(self, selector, timeout=60):
        
        try:
            wait = WebDriverWait(self.chrome, timeout)
            loc = (By.CSS_SELECTOR, selector)
            wait.until(EC.presence_of_element_located(loc))
            wait.until(EC.visibility_of_element_located(loc))
            return self.chrome.find_element_by_css_selector(selector)
        except TimeoutException as e:
            self.screenshot('error.png')
            raise e
            
    def _element_exists_at(self, selector, timeout=None):
        return self._wait_for(selector, timeout) is not None
        
    def _check_valid_qrcode(self):
        # Not logged in
        small_timeout = 5
        while not self._element_exists_at(self.selectors['search_input'], timeout=small_timeout):
            qrcode = self._wait_for(self.selectors['qrcode'], timeout=small_timeout)
            self.screenshot('qrcode.png')
            
            print('Look for whatsapp QRCode inside your running directory.')
            sleep(small_timeout)
        
        print('Whatsapp successfully logged in...')
        self.screenshot('screens/1.png')

    def _search_for_chat(self, to):
        self._wait_for(self.selectors['search_input']).send_keys(to)
        self._wait_for(self.selectors['search_result'].format(to)).click()
        self.screenshot('screens/2.png')
    
    def _type_message(self, message):
        self._wait_for(self.selectors['message_input']).send_keys(message + '\n')
        # self._wait_for(selectors['message_send']).click()  # replaced by '\n' on previous line
        self.screenshot('screens/3.png')
        
    def screenshot(self, path):
        return self.chrome.get_screenshot_as_file(path)
    
    def send(self, message, to):
        
        try:
            self._check_valid_qrcode()
            self._search_for_chat(to)
            self._type_message(message)
            
        except Exception as e:
            print('An unexpected error occured. Quiting chrome now')
            self.screenshot('screens/error.png')
            
            raise e
            
            
    def get_chats(self):
        '''
            return contact name for every chat open
        '''
        
        sel = '#side span[dir=auto][title]'
        chats = self.chrome.find_elements_by_css_selector(sel)
        
        for chat in chats:
            print(chat.text)
        
        return [chat.text for chat in chats]
        
    def get_contacts(self):
        '''
            return contact name for every chat open
        '''
        
        contacts = []
        
        try:
            self.chrome.find_element_by_css_selector('#app span[data-icon=chat]').click()
        except:
            pass
        
        c_list = [None]
        while not set(c_list).issubset(set(contacts)):
            c_elements = self.chrome.find_elements_by_css_selector('#app span[dir=auto][title]')
            c_list = [e.text for e in c_elements]
            
            for c in c_list:
                if c not in contacts:
                    contacts.append(c)
                 
            sel = '#app span div._1vDUw'  
            el = self.chrome.find_element_by_css_selector(sel)
            el.send_keys(Keys.PAGE_DOWN)
                
            
            # script = 'var sel = "#app span div[data-list-scroll-offset=true]"; ' + \
            #          'var app = document.querySelector(sel).parentElement; ' + \
            #          'app.scrollTo(0, app.scrollHeight);'
            
            # self.chrome.execute_script(script)
            
        
        return contacts
        

if __name__ == '__main__':
    message = 'whatsapp-bot ' + str(datetime.now())
    to = 'Saldo Contas'
    
    whats = Whatsapp()
    # whats.send(message, to)
    