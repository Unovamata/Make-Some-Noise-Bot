import time
import keyboard
import config
import random
import ctypes

contentList = []

with open(config.filepath, 'r') as file:
    contentList = file.readlines()

contentList = [float(line.strip()) for line in contentList]
random.shuffle(contentList);

config.CountdownCaller()

isFirstKey = True
breakWhile = False
firstKey, secondKey = config.VK_CODE.get(config.firstKey), config.VK_CODE.get(config.secondKey)
waitTimeMultiplicator = random.randrange(60, 65)

while True:
    for lineTime in contentList:
        if keyboard.is_pressed(' '):
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


    if breakWhile:
        break