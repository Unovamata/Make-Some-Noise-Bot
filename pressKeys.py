import time
import keyboard
import config
import random
import ctypes
import pyautogui
import cv2
from PIL import Image
import pytesseract
import numpy as np

contentList = []

with open(config.filepath, 'r') as file:
    contentList = file.readlines()

contentList = [float(line.strip()) for line in contentList]

config.CountdownCaller()

isFirstKey = True
breakWhile = False

customConfig = r'--oem 3 --psm 7'
checkForScore = 0

def ScrollToPosition(result):
    if result is not None:
        left, top, width, height = result

        centerX = left + width // 2
        centerY = top + height // 2

        return centerX, centerY
    return None

def GetKeysFromImage(keyImage):
    gray = cv2.cvtColor(np.array(keyImage), cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    key = pytesseract.image_to_string(binary_image, lang='eng', config='--psm 6')

    key = key.replace(" ", "").replace("\n", "")
    key = key[0]
    return key

firstKey, secondKey = None, None

def GetKeys(first, second):
    global firstKey, secondKey

    firstKey, secondKey = config.VK_CODE.get(ord(first)), config.VK_CODE.get(ord(second))

firstKeyPress, secondKeyPress = None, None

while True:
    print("Looking the Start Game Button...")
    """while True:
        # Find the start game button
        startGameFound = pyautogui.locate(config.startGameImage, config.TakeScreenshot(), confidence=0.6)
        mousePosition = ScrollToPosition(startGameFound)

        if mousePosition is not None:
            pyautogui.moveTo(mousePosition, duration=random.uniform(0.8, 1.2), tween=pyautogui.easeInOutQuad)

        if mousePosition == pyautogui.position():
            pyautogui.leftClick()
            break"""

    print("Looking for key image...")

    screenshot = config.TakeScreenshot()
    keysString = []

    for index, key in enumerate(pyautogui.locateAll(config.keyImage, screenshot, confidence=0.8)):
        left, top, width, height = key
        left += 10
        top += 10
        width -= 20
        height -= 20
        screenshotRegion = Image.fromarray(screenshot).crop((left, top, left + width, top + height))

        if index == 0:
            firstKeyPress = GetKeysFromImage(screenshotRegion)
        else:
            secondKeyPress = GetKeysFromImage(screenshotRegion)

    print("Key images found!")
    print("Keys found! Key 1:" + str(firstKeyPress) + " | Key 2:" + str(secondKeyPress) + " |")
    firstKey = config.VK_CODE.get(firstKeyPress)
    secondKey = config.VK_CODE.get(secondKeyPress)
    print(firstKey, secondKey)

    # Reset values
    waitTimeMultiplicator = random.randrange(55, 65)
    random.shuffle(contentList)
    score = 0
    scoreScreenshot = None
    scoreString = ""

    print("Pressing keys!")
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
            scoreScreenshot = config.TakeScreenshotInRegion(config.selectTopLeft, config.selectBottomRight)
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