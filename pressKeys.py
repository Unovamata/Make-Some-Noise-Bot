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

customConfig = r'--oem 3 --psm 7'
checkForScore = 0

while True:
    waitTimeMultiplicator = random.randrange(60, 70)
    random.shuffle(contentList)
    score = 0
    scoreScreenshot = None
    scoreString = ""

    for lineTime in contentList:
        if keyboard.is_pressed('0'):
            breakWhile = True
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

        if checkForScore >= config.checkIterationThreshold:
            scoreScreenshot = config.TakeScreenshotInRegion(config.topLeft, config.bottomRight)
            scoreString = pytesseract.image_to_string(scoreScreenshot, config=customConfig)
            checkForScore = 0

        checkForScore += 1

        try:
            score = int(scoreString)
            
            if score >= config.scoreThreshold:
                ctypes.windll.user32.keybd_event(config.VK_CODE.get(' '), 0, 0, 0)
                break

        except:
            score = 0

    if breakWhile:
        break

    GetKeys()
    firstKey, secondKey = config.VK_CODE.get(config.firstKey), config.VK_CODE.get(config.secondKey)