# ----setup
from picamera import PiCamera
from sense_hat import SenseHat
from time import sleep
import time
import pygame

deurbel = SenseHat()
camera = PiCamera()
# -----waarden
# opslag
music_bel = "bell.mp3" # musiek bestand bel toon
music_click = "camera_click.mp3" # musiek bestand click
locatie = '.' # map fotos
vertraging = 20000 # snelheid knop animatie

# kleuren
r = [255, 0, 0] # rood
g = [0, 255, 0] # groen
b = [0, 0, 255] # blauw
G = [255, 255, 0] # geel
f = [160, 160, 160] # grijz
# figuren
bel = [
b,b,b,G,G,b,b,b,
b,b,b,G,G,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,G,G,b,b,b,
b,b,G,G,G,G,b,b,
b,b,G,G,G,G,b,b,
b,G,G,G,G,G,G,b,
b,b,b,b,b,b,b,b,
]

blue_screen = [
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
]

foto_logo = [
b,b,b,b,b,b,b,b,
b,b,b,b,b,r,r,b,
b,f,f,f,f,f,f,b,
b,f,f,g,g,f,f,b,
b,f,f,g,g,f,f,b,
b,f,f,f,f,f,f,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
]

knop = [
[
b,b,b,g,g,g,b,b,
b,b,g,g,g,g,g,b,
b,b,b,g,g,g,b,b,
b,b,b,b,g,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,r,r,r,r,r,r,b,
G,G,G,G,G,G,G,G,
],[
b,b,b,g,g,g,b,b,
b,b,b,g,g,g,b,b,
b,b,g,g,g,g,g,b,
b,b,b,g,g,g,b,b,
b,b,b,b,g,b,b,b,
b,b,b,b,b,b,b,b,
b,r,r,r,r,r,r,b,
G,G,G,G,G,G,G,G,
],[
b,b,b,g,g,g,b,b,
b,b,b,g,g,g,b,b,
b,b,b,g,g,g,b,b,
b,b,g,g,g,g,g,b,
b,b,b,g,g,g,b,b,
b,b,b,b,g,b,b,b,
b,r,r,r,r,r,r,b,
G,G,G,G,G,G,G,G,
],[
b,b,b,g,g,g,b,b,
b,b,b,g,g,g,b,b,
b,b,b,g,g,g,b,b,
b,b,b,g,g,g,b,b,
b,b,g,g,g,g,g,b,
b,b,b,g,g,g,b,b,
b,b,b,b,g,b,b,b,
G,G,G,G,G,G,G,G,
]]


# -----subs
def geluid_start_bel():
    pygame.mixer.init()
    pygame.mixer.music.load(music_bel)
    pygame.mixer.music.play(loops=-1)
    #while pygame.mixer.music.get_busy() == True:
    #    continue

def geluid_click():
    pygame.mixer.init()
    pygame.mixer.music.load(music_click)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue


def geluid_stop():
    pygame.mixer.music.stop()

def tellen(i,wacht):
    for q in range(1,i+1):
        deurbel.show_letter(str(q),text_colour=G,back_colour=b)
        sleep(wacht)

def foto():
    print("foto maken")
    deurbel.show_message("Cheese!!!",text_colour=G,back_colour=b,scroll_speed=0.1)
    tellen(3,0.4)
    deurbel.set_pixels(foto_logo)
    sleep(0.4)
    geluid_click()
    # --- foto maken
    camera.start_preview()
    camera.capture(locatie+'/image_' + time.strftime("%Y-%m-%d_%H-%M-%S") + '.jpg')
    camera.stop_preview()

def animatie(keer):
    q=0
    for q in range(0,keer):
        deurbel.set_pixels(bel)
        sleep(0.5)
        deurbel.set_pixels(blue_screen)
        sleep(0.2)

def oproep():
    # --- foto maken
    foto()
    sleep(0.3)
    # --- foto start
    geluid_start_bel()
    # --- animatie en geluid
    animatie(8)
    # stop geluid
    geluid_stop()

# -----programa
exit = 0
frame = 0
traag= 0
while exit == 0:
    # joystick input
    for joystick in deurbel.stick.get_events():
        if joystick.action == "released":
            if joystick.direction == "left":
                exit = 1;
            elif joystick.direction == "middle":
                oproep()
            deurbel.set_pixels(blue_screen)
    # knop animatie
    traag=traag+1
    if traag >= vertraging:
        traag=0
        deurbel.set_pixels(knop[frame])
        frame=frame+1
        if frame >= 4:
            frame=0

# -----Einde programa
deurbel.clear()
