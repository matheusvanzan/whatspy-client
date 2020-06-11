# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse

# from chromepy.chrome import Chrome
from chromepy.remote import ChromeRemote
from api.whatspy import Whatsapp


URL = 'https://web.whatsapp.com'
SCREEN = 'screen.png'

def teste(request):
    
    chrome = ChromeRemote()
    
    sel = '#side span[dir=auto][title]'
    chats = chrome.find_elements_by_css_selector(sel)
    for chat in chats:
        print(chat.text)
        
    return HttpResponse(chats)

def screenshot(request):
    
    remote = ChromeRemote()
    remote.get_screenshot_as_file(SCREEN)
    
    return HttpResponse(open(SCREEN, 'rb').read(), content_type = 'image/jpeg')
    
def index(request):
    whats = Whatsapp()
    data = {
        'default': datetime.now(),
        'chats': whats.get_chats(),
        'contacts': whats.get_contacts()
    }
    return render(request, 'api/index.html', data)
    
def send(request):
    print(request.GET)
    
    to = request.GET['to']
    message = request.GET['message']
    
    try:
        whats = Whatsapp()
        whats.send(message, to)
        return HttpResponse('1')
    except:
        # /send/?to=Matheus%20Vanzan&message=teste
        return HttpResponse('0')
    
    