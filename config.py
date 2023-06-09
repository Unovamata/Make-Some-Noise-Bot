import time
import pyautogui
import cv2
import numpy as np

# Keys to press;
firstKey, secondKey = input("Press usable keys: ")
firstKeyCode = ord(firstKey)
secondKeyCode = ord(secondKey)

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

def MouseEventHandler(event, x, y, flags, param):
    global topLeft, bottomRight

    if event == cv2.EVENT_LBUTTONDOWN:
        topLeft = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        bottomRight = (x, y)
        cv2.destroyAllWindows()

# Create a window that will handle the mouse up and down event
windowName = "Select Area"
cv2.namedWindow(windowName)
cv2.setMouseCallback(windowName, MouseEventHandler)

screenshot = pyautogui.screenshot()
screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

while True:
    cv2.imshow(windowName, screenshot)
    if(cv2.waitKey(1) & 0xFF == ord("q")):
        break

x1, y1 = topLeft
x2, y2 = bottomRight

selectedRegion = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
selectedRegion.save("region.png")
