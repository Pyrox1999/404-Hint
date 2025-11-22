import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
import random
import pgzrun
import pygame
import requests

pygame.mixer.music.load("song.ogg") #Eric Matyas
pygame.mixer.music.play(-1)

level = -2
target = "http://127.0.0.1"
message=""
gemacht=False

def analyze_url(url):
    global message
    try:
        response = requests.get(url)
        message+=f"URL: {url}\n"
        message+=f"Status Code: {response.status_code}\n"

        if response.status_code == 404:
            message+="→ 404 Not Found detected.\n"
            if "WordPress" in response.text:
                message+="⚡ Hint: Page seems to use WordPress.\n"
            elif "nginx" in response.text.lower() or "nginx" in response.headers.get("Server","").lower():
                message+="⚡ Hint: 404-Page seems to be Nginx.\n"
            elif "Apache" in response.text or "apache" in response.headers.get("Server","").lower():
                message+="⚡ Hint: Error-Page is maybe Apache.\n"
            elif "IIS" in response.text or "microsoft-iis" in response.headers.get("Server","").lower():
                message+="⚡ Hint: Microsoft IIS recognized."
            elif "Drupal" in response.text:
                message+="⚡ Hint:  Page seems to use Drupal.\n"
            elif "Joomla" in response.text:
                message+="⚡ Hint: Page is maybe Joomla.\n"
            elif "Django" in response.text.lower():
                message+="⚡ Hint: Django-Framework recognized.\n"
            elif "Rails" in response.text or "Ruby on Rails" in response.text:
                message+="⚡ Hint: Ruby on Rails recognized.\n"
            elif "ASP.NET" in response.text or "asp.net" in response.headers.get("X-Powered-By","").lower():
                message+="⚡ Hint: ASP.NET recognized.\n"
            elif "Tomcat" in response.text or "tomcat" in response.headers.get("Server","").lower():
                message+="⚡ Hint: Apache Tomcat recognized.\n"
            else:
                message+="ℹ️ No special hints found.\n"
        
        else:
            message+="→ No 404, Page answers with other status.\n"
    except Exception as e:
        message+=f"Error on load: {e}\n"

def draw():
    global level, target,message
    screen.clear()
    if level==-2:
        screen.blit("disclaimer",(0,0))
    if level == -1:
        screen.blit("title", (0, 0))
    elif level == 0:
        screen.blit("intro", (0, 0))
    elif level == 1:
        screen.blit("back", (0, 0))
        screen.draw.text("Enter Website:", center=(400, 130), fontsize=24, color=(25, 200, 255))
        screen.draw.text(target, center=(400, 180), fontsize=24, color=(255, 255, 0))
    elif level == 2:
        screen.blit("back",(0,0))
        screen.draw.text(message, center=(400, 180), fontsize=24, color=(255, 255, 0))

def on_key_down(key, unicode=None):
    global level, target
    if key==keys.ESCAPE:
        pygame.quit()
    if key == keys.BACKSPACE:
        target = ""
    elif key == keys.RETURN and level == 1:
        if not target.strip():
            target = "127.0.0.1/bloedsinnxyz"
        target+="/bloedsinnxychu"
        level = 2
    elif unicode and key != keys.RETURN and level==1:
        target += unicode

def update():
    global level,target,gemacht
    if (level == 0 or level==-2) and keyboard.RETURN:
        level +=1
    elif level -1 and keyboard.space:
        level = 0
    if level==2:
        if not gemacht:
            analyze_url(target)
            gemacht=True
        if keyboard.space:
            level=0

pgzrun.go()



