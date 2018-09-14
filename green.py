from sense_hat import SenseHat
from time import sleep
import os

sense = SenseHat()

red = (255,0,0)
green = (0,255,0)

sense.clear (green)

sleep(5)
    
sense.clear (0,0,0)

os.system('python DeurbelV7.py')