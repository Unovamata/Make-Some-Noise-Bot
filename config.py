import time
import keyboard
import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab, Image
import pytesseract
import random

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Image recognition loading
startGameImage = Image.open("Start Game.png")
submitPointsImage = Image.open("Submit Points.png")
closeImage = Image.open("Close.png")
keyImage = Image.open("Key.png")

# Score threshold
scoreThreshold = 2700
checkIterationThreshold = random.randrange(30, 50)

VK_CODE = {
    'A': 0x41, 'B': 0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45,
    'F': 0x46, 'G': 0x47, 'H': 0x48, 'I': 0x49, 'J': 0x4A,
    'K': 0x4B, 'L': 0x4C, 'M': 0x4D, 'N': 0x4E, 'O': 0x4F,
    'P': 0x50, 'Q': 0x51, 'R': 0x52, 'S': 0x53, 'T': 0x54,
    'U': 0x55, 'V': 0x56, 'W': 0x57, 'X': 0x58, 'Y': 0x59,
    'Z': 0x5A, ' ': 0x20
}

# Adding lower case values;
VK_CODE.update({key.lower(): value for key, value in VK_CODE.items()})

# File path with key press times
filepath = "timestamps.txt"

# The time to wait for the script to start
countdown = [3, 2, 1, 'GO!']


def CountdownCaller():
    for item in countdown:
        print(item)
        time.sleep(1)


# Selecting the screenshot area
topLeft, bottomRight = None, None
selecting = False

# Take a screenshot of the entire screen;
def TakeScreenshot():
    screenshot = ImageGrab.grab()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot

clone = TakeScreenshot()

# Mouse manager function for reading coordinates based on events
def MouseEventHandler(event, x, y, flags, param):
    global topLeft, bottomRight, selecting

    if event == cv2.EVENT_LBUTTONDOWN:
        topLeft = (x, y)
        selecting = True
    elif event == cv2.EVENT_LBUTTONUP:
        selecting = False

def OpenSelectionWindow(name):
    global bottomRight

    # Create a window that will handle the mouse up and down event
    windowName = name + ". (Update Screenshot by Pressing 'S', Save the changes with 'Q')"
    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, MouseEventHandler)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    clone = None # Screenshot taken

    # Screenshot updating and data saving
    while True:
        # If the clone is not null, allow me to draw a rectangle:
        if clone is not None:
            if selecting:
                cv2.rectangle(clone, topLeft, pyautogui.position(), (0, 255, 0), 2)
                bottomRight = pyautogui.position()
            cv2.imshow(windowName, clone)
        else:
            clone = TakeScreenshot()

        eraseKey = keyboard.is_pressed('S')

        if eraseKey:
            clone = None

        breakKey = cv2.waitKey(1) & 0xFF == ord("q")

        if breakKey:
            break

    cv2.destroyAllWindows()

OpenSelectionWindow("Select Score Area")
selectTopLeft, selectBottomRight = topLeft, bottomRight

def TakeScreenshotInRegion(top, bottom):
    x1, y1 = top
    x2, y2 = bottom
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)

    selectedRegion = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    return selectedRegion
