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
import matplotlib.pyplot as plt

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

        centerX = left + width // 1.2
        centerY = top + height // 1.2

        return centerX, centerY
    return None

firstKey, secondKey = None, None
firstKeyPress, secondKeyPress = None, None

def FindImage(image, confidence, mode='single', click=True):
    while True:
        try:
            screenshot = config.TakeScreenshot()

            if mode == 'single':
                element = pyautogui.locate(image, screenshot, confidence=confidence)
                
                if element:
                    if click:
                        mousePosition = ScrollToPosition(element)
                    
                        if mousePosition is not None:
                            pyautogui.moveTo(mousePosition, duration=random.uniform(0.5, 1.2), tween=pyautogui.easeInOutQuad)
                            if mousePosition == pyautogui.position():
                                pyautogui.leftClick()

                    return True
                    
            elif mode == 'multiple':
                # Convert images to grayscale
                key = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
                instances = []

                while True:
                    # Initiate SIFT detector
                    sift = cv2.SIFT_create()

                    # Find the keypoints and descriptors with SIFT
                    kp1, des1 = sift.detectAndCompute(key, None)
                    kp2, des2 = sift.detectAndCompute(screenshot, None)

                    # BFMatcher with default params
                    bf = cv2.BFMatcher()
                    matches = bf.knnMatch(des1, des2, k=2)

                    # Apply ratio test
                    good = []
                    for m, n in matches:
                        if m.distance < 0.75 * n.distance:
                            good.append(m)

                    # Get the matching keypoints
                    points1 = np.zeros((len(good), 2), dtype=np.float32)
                    points2 = np.zeros((len(good), 2), dtype=np.float32)

                    for i, match in enumerate(good):
                        points1[i, :] = kp1[match.queryIdx].pt
                        points2[i, :] = kp2[match.trainIdx].pt

                    # Find the bounding box
                    if len(points1) > 0:
                        left, top = np.min(points2, axis=0)
                        width, height = np.max(points2, axis=0)

                        keyImage = screenshot[int(top + 4):int(height - 6), int(left + 2):int(width - 2)]
                        keyImage = cv2.cvtColor(np.array(keyImage), cv2.COLOR_GRAY2BGR)

                        instances.append(keyImage)

                        left -= 10
                        top -= 10
                        width += 20
                        height += 20

                        # Draw bounding boxes on the images
                        screenshot = cv2.rectangle(screenshot, (int(left), int(top)), (int(width), int(height)), (0, 255, 0), thickness=-1)

                        if len(instances) >= 2:
                            break

                return instances
        except:
            continue


# Loop parameters
breakWhile = False
keysFailsafe = False
isFirstKey = True
checkForScore = 0
gamesPlayed = 0
gamesUntilSleep = random.randint(20, 50)
zeroScores = 0

while True:
    # Not allowing the bot to go infinitely as there's a limit to the scores that can be submitted
    print(f"Games played: {gamesPlayed} of {config.gamesToPlay}")
    gamesPlayed += 1
    if gamesPlayed > config.gamesToPlay:
        break

    if gamesPlayed >= gamesUntilSleep:
        sleepTime = random.uniform(120, 300)
        gamesUntilSleep += random.randint(30, 60)
        print(f"Sleeping for {int(sleepTime / 60)} minutes...")
        time.sleep(sleepTime)


    print("Looking the Start Game Button...")
    FindImage(config.startGameImage, 0.4)

    print("Looking for key image...")
    firstKeyPress, secondKeyPress = None, None

    resetWhile = False

    def GetKeysFromImage(keyImage):
        gray = cv2.cvtColor(np.array(keyImage), cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        customConfig = r'--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        keyFormat = pytesseract.image_to_string(binary_image, lang='eng', config=customConfig)

        keyFormat = keyFormat.strip()

        # Ensure keyFormat contains only letters
        if len(keyFormat) > 0 and keyFormat[0].isalpha():
            return keyFormat[0].upper()  # Ensure uppercase
        
        return None

    # If the key is not valid, simply exit the current loop early and go to the next iteration
    def ExitEarly():
        global resetWhile

        ctypes.windll.user32.keybd_event(config.VK_CODE.get(' '), 0, 0, 0)
        FindImage(config.restartGameImage, confidence=0.6, click=True)
        resetWhile = True
        print("Key images could not be found... Restarting...")

    def RecursiveDetectKey(key, keyImage, depth = 0, maxDepth = 2, isSecond = False):
        if depth >= maxDepth:
            ExitEarly()
            return None

        if key is None:
            key = GetKeysFromImage(keyImage)

            if isSecond and firstKeyPress == secondKeyPress:
                key = None

            if key is None:
                return RecursiveDetectKey(key, keyImage, depth + 1, maxDepth)
            
        return key

    while True:
        screenshot = config.TakeScreenshot()
        keysString = []

        firstKeyPress = None
        secondKeyPress = None

        imagesFound = FindImage(config.keyImage, confidence=0.8, mode='multiple')

        if len(imagesFound) <= 1:
            resetWhile = True
            ExitEarly()
            break

        # Find the locations of the key image in the screenshot
        for index, key in enumerate(imagesFound):
            
            # Process the cropped region
            if index == 0 and firstKeyPress is None:
                firstKeyPress = RecursiveDetectKey(firstKeyPress, key, 0, 2)
                    
            elif index == 1 and secondKeyPress is None:
                secondKeyPress = RecursiveDetectKey(secondKeyPress, key, 0, 2, isSecond = True)

                if secondKeyPress == firstKeyPress:
                    ExitEarly()

        # Check if both keys are valid
        if firstKeyPress is not None and secondKeyPress is not None or resetWhile:
            break

    if resetWhile:
        continue

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
    zeroScores = 0
    maxFailedCycles = 2

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
                if(zeroScores >= maxFailedCycles):
                    raise ValueError("Invalid score")

                # Strip whitespace and remove non-digit characters
                scoreString = ''.join(filter(str.isdigit, scoreString.strip()))
                
                # Convert to integer if the string is not empty, otherwise set score to 0
                score = int(scoreString) if scoreString else 0
                print(f"Current Score {score}")

                if(score == 0): 
                    zeroScores += 1

                # If the score is what is needed, press the space bar to send the score
                if score >= config.scoreThreshold:
                    ctypes.windll.user32.keybd_event(config.VK_CODE.get(' '), 0, 0, 0)
                    break
            # If it was not possible, the score may not be parseable
            except Exception as e:
                score = 0
                zeroScores = 0
                ctypes.windll.user32.keybd_event(config.VK_CODE.get(' '), 0, 0, 0)

                if FindImage(config.restartGameImage, confidence=0.4, click=True):
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
        FindImage(config.submitPointsImage, 0.4)

print("Stopped execution")