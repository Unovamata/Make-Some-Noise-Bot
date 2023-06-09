import time
import keyboard
import config
import random
import ctypes
import pyautogui
from PIL import Image
import pytesseract

contentList = []

with open(config.filepath, 'r') as file:
    contentList = file.readlines()

contentList = [float(line.strip()) for line in contentList]

config.CountdownCaller()

isFirstKey = True
breakWhile = False
firstKey, secondKey = config.VK_CODE.get(config.firstKey), config.VK_CODE.get(config.secondKey)

def GetKeys():
    config.firstKey, config.secondKey = input("Press usable keys: ")
    config.firstKeyCode = ord(config.firstKey)
    config.secondKeyCode = ord(config.secondKey)

while True:
    waitTimeMultiplicator = random.randrange(60, 70)
    random.shuffle(contentList);
    
    for lineTime in contentList:
        if keyboard.is_pressed('0'):
            breakWhile = True
            break
        elif keyboard.is_pressed(' '):
            break

        if isFirstKey:
            ctypes.windll.user32.keybd_event(firstKey, 0, 0, 0)
            time.sleep(lineTime * waitTimeMultiplicator)
            ctypes.windll.user32.keybd_event(firstKey, 0, 2, 0)
            isFirstKey = False
        else:
            ctypes.windll.user32.keybd_event(secondKey, 0, 0, 0)
            time.sleep(lineTime * waitTimeMultiplicator)
            ctypes.windll.user32.keybd_event(secondKey, 0, 2, 0)
            isFirstKey = True

    if breakWhile:
        break

    GetKeys()
    firstKey, secondKey = config.VK_CODE.get(config.firstKey), config.VK_CODE.get(config.secondKey)