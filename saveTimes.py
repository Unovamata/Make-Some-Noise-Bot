import time
import keyboard
import config

config.CountdownCaller()

def SaveTime():
    elapsedTime = time.time() - startTime
    if(elapsedTime != 0.0):
        timestamps.append(elapsedTime)
        print(elapsedTime)

startTime = 0
timestamps = []

while True:
    startTime = time.time()

    if keyboard.is_pressed(' '):
        break
    else:
        if keyboard.is_pressed(config.firstKey) or keyboard.is_pressed(config.secondKey):
            SaveTime()

# Saving the inputs in a text file for later reference
with open(config.filepath, 'a') as file:
    for timestamp in timestamps:
        file.write(f"{timestamp}\n")

print('Keys Saved!')