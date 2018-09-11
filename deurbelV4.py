
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
music = "train.mp3" # musiek bestand
locatie = '/home/pi/Desktop/Deurbel' # map fotos

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

menu_screen = [
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,b,b,
b,b,b,b,b,b,r,b,
r,b,b,G,G,b,r,r,
b,b,b,G,G,b,r,r,
b,b,b,b,b,b,r,b,
b,b,g,g,g,g,b,b,
b,b,b,g,g,b,b,b,
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


# -----subs
def geluid_start():
    pygame.mixer.init()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()
    #while pygame.mixer.music.get_busy() == True:
    #    continue

def geluid_stop():
    pygame.mixer.music.stop()

def foto():
    # --- vertelt gebruiker dat er een foto wordt gemaakt
    print("foto maken")
    deurbel.show_message("Cheese!!!",text_colour=G,back_colour=b,scroll_speed=0.1)
    deurbel.set_pixels(foto_logo)
    sleep(0.5)
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

def rang():
    # --- foto start
    geluid_start()
    # --- foto maken
    foto()
    # --- animatie en geluid
    animatie(8)
    # stop geluid
    geluid_stop()

def show(wat):
    if wat == 1:
        deurbel.show_message("%sC" % round(deurbel.get_temperature(),1))

# -----programa loop
deurbel.set_pixels(blue_screen)
exit = 0
while exit == 0:
    joystick = deurbel.stick.wait_for_event()
    if joystick.action == "released":
        if joystick.direction == "left":
            exit = 1;
        elif joystick.direction == "middle":
            rang()
        elif joystick.direction == "right":
            show(1)
        deurbel.set_pixels(menu_screen)

# -----Einde programa
deurbel.clear()
