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

# Load timestamp list for key presses
contentList = []

with open(config.filepath, 'r') as file:
    contentList = file.readlines()

contentList = [float(line.strip()) for line in contentList]

# Setting up a countdown after start
config.CountdownCaller()

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

    customConfig = r'--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    keyFormat = pytesseract.image_to_string(binary_image, lang='eng', config=customConfig)

    keyFormat = keyFormat.replace(" ", "").replace("\n", "")

    try:
        keyFormat = keyFormat[0]
    except:
        keyFormat = ""

    return keyFormat

firstKey, secondKey = None, None
firstKeyPress, secondKeyPress = None, None

def GetKeys(first, second):
    global firstKey, secondKey

    firstKey, secondKey = config.VK_CODE.get(ord(first)), config.VK_CODE.get(ord(second))

def FindImageAndMoveMouseTo(image):
    while True:
        # Find the start game button
        startGameFound = pyautogui.locate(image, config.TakeScreenshot(), confidence=0.6)
        mousePosition = ScrollToPosition(startGameFound)

        if mousePosition is not None:
            pyautogui.moveTo(mousePosition, duration=random.uniform(0.5, 1.2), tween=pyautogui.easeInOutQuad)

        if mousePosition == pyautogui.position():
            pyautogui.leftClick()
            break

# Loop parameters
breakWhile = False
keysFailsafe = False
isFirstKey = True
checkForScore = 0
gamesPlayed = 0
gamesUntilSleep = random.randint(20, 50)

while True:
    # Not allowing the bot to go infinitely as there's a limit to the scores that can be submitted
    print(f"Games played: {gamesPlayed} of {config.gamesToPlay}")
    gamesPlayed += 1
    if gamesPlayed > config.gamesToPlay:
        break

    if gamesPlayed >= gamesUntilSleep:
        sleepTime = random.uniform(120, 300)
        gamesUntilSleep = random.randint(5, 30)
        print(f"Sleeping for {int(sleepTime / 60)} minutes...")
        time.sleep(sleepTime)

    print("Looking the Start Game Button...")
    FindImageAndMoveMouseTo(config.startGameImage)

    print("Looking for key image...")
    firstKeyPress, secondKeyPress = None, None

    # Search keys in a screenshot
    while True:
        screenshot = config.TakeScreenshot()
        keysString = []

        for index, key in enumerate(pyautogui.locateAll(config.keyImage, screenshot, confidence=0.6)):
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

        if firstKeyPress is not None and secondKeyPress is not None:
            if firstKeyPress != ' ' and secondKeyPress != ' ':
                break

    # Key configuration
    print("Key images found!")
    print("Keys found! Key 1:" + str(firstKeyPress) + " | Key 2:" + str(secondKeyPress) + " |")
    firstKey = config.VK_CODE.get(firstKeyPress)
    secondKey = config.VK_CODE.get(secondKeyPress)

    # Reset values
    config.checkIterationThreshold = random.randrange(30, 45)
    waitTimeMultiplicator = random.randrange(55, 65)
    random.shuffle(contentList)
    score = 0
    scoreScreenshot = None
    scoreString = ""
    keysFailsafe = False

    print("Pressing keys!")
    for lineTime in contentList:
        if keyboard.is_pressed('0'):
            breakWhile = True
            break

        # Press firstKey and then sleep
        if isFirstKey:
            ctypes.windll.user32.keybd_event(firstKey, 0, 0, 0)
            time.sleep(lineTime * waitTimeMultiplicator)
            ctypes.windll.user32.keybd_event(firstKey, 0, 2, 0)
            isFirstKey = False
        # Press secondKey and then sleep
        else:
            ctypes.windll.user32.keybd_event(secondKey, 0, 0, 0)
            time.sleep(lineTime * waitTimeMultiplicator)
            ctypes.windll.user32.keybd_event(secondKey, 0, 2, 0)
            isFirstKey = True

        # Check if it's time to check the score
        if checkForScore >= config.checkIterationThreshold:
            # If that's the case, take a screenshot of the score area, and then, convert it to text
            scoreScreenshot = config.TakeScreenshotInRegion(config.selectTopLeft, config.selectBottomRight)
            scoreString = pytesseract.image_to_string(scoreScreenshot, config= r'--oem 3 --psm 7')

            # If it's possible, convert the text to an integer, and break the loop if possible
            try:
                score = int(scoreString)

                # If the score is what is needed, press the space bar to send the score
                if score >= config.scoreThreshold:
                    ctypes.windll.user32.keybd_event(config.VK_CODE.get(' '), 0, 0, 0)
                    break
                else:
                    if pyautogui.locate(config.restartGameImage, config.TakeScreenshot(), confidence=0.6):
                        keysFailsafe = True
                        break
            # If it was not possible, the score may not be parseable
            except:
                score = 0

                if pyautogui.locate(config.restartGameImage, config.TakeScreenshot(), confidence=0.6):
                    keysFailsafe = True
                    break

            checkForScore = 0 # and reset the threshold

        # Augment the score checking threshold
        checkForScore += 1

    # Break the loop if set to be broken
    if breakWhile:
        break

    # Find the submit points image
    if keysFailsafe is False:
        print("Submitting points...")
        FindImageAndMoveMouseTo(config.submitPointsImage)

        # Close the game window as soon as it is found, as the score sending is an async task in the page
        print("Closing the submit window...")
        FindImageAndMoveMouseTo(config.closeImage)
    else:
        print("Keys were not recognized correctly, restarting...")
        gamesPlayed -= 1
        FindImageAndMoveMouseTo(config.restartGameImage)

print("Stopped execution")