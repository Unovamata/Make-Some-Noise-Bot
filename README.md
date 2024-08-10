<p align="center">
  <img src="https://raw.githubusercontent.com/Unovamata/Make-Some-Noise-Bot/main/Wiki/banner.png" />
</p>

# Altador Cup - Make Some Noise!! Bot

I made this bot to automatically play the "Make Some Noise!!" minigame during the Altador Cup site event on Neopets. This bot has computer vision to automatically send scores, detect keys to press, waiting to simulate breaks after a set number of submitted scores, and correct itself if any error occurred during the execution of the bot.
 
**Table of Contents**

+ [Dependencies](#dependencies)
+ [Setup](#setup)
+ [Botting](#botting)

# Dependencies
+ [Python](https://www.python.org/downloads/)
+ [TesseractOCR](https://github.com/UB-Mannheim/tesseract/wiki)

For this, you must download the installer and execute it in your machine. Do not change the default installation folder, else this program will not work. When you navigate to the Tesseract page, make sure to find the following **setup.exe** URL.

<p align="center">
  <img src="https://raw.githubusercontent.com/Unovamata/Make-Some-Noise-Bot/main/Wiki/tesseract.png" />
</p>

+ Keyboard
+ Pillow
+ OpenCV
+ Numpy
+ PyAutoGUI

# Setup

+ Download the "Make Some Noise!!" bot source files in the [Releases](https://github.com/Unovamata/Make-Some-Noise-Bot/releases/latest) page.
+ Download the files above and install TesseractOCR and Python.
+ Make sure you configure the PATH for Python and [TesseractOCR](https://www.youtube.com/watch?v=2kWvk4C1pMo). In the case of Python you can do this through the installer. **Read carefully to not skip this step.**
+ Once you have installed Python and configured its respective **"Environment Variable"**, run the **"install dependencies.bat"** file. This file will install all the libraries Python needs tp run the bot.
+ After the **"install dependencies.bat"** window closes, open the **"run.bat"** file in the bot's files.
+ A new window will open. You're now ready to configure the bot to play the game for you.
+ Set your display resolution to **1366x768** and set the zoom of the minigame page to **100%** if the script gives you any troubles.

# Botting

<p align="center">
  <img src="https://raw.githubusercontent.com/Unovamata/Make-Some-Noise-Bot/main/Wiki/Window Tutorial 1.png" />
</p>

+ This bot uses screenshots to "read" information regarding the "Make Some Noise!!" minigame. This data is hosted locally and it won't leave your machine. To update this screenshot, you have to press the **"S"** key in the window were the game is at. The window does not have to be active for this updated screenshot to appear.
+ Make sure the window where the "Make Some Noise!!" minigame is at is maximized, keyword: **window** not the minigame itself.
+ Start the game and once you can see the **"Score: 0"** GUI element, press **"S"** in your keyboard to update the current screenshot.

<p align="center">
  <img src="https://raw.githubusercontent.com/Unovamata/Make-Some-Noise-Bot/main/Wiki/Window Tutorial 2.png" />
</p>

Press the **"S"** key in this window.

+ Return to the bot window and you'll notice that the app took a screenshot of your desktop.
+ Drag your mouse from the start of the points number to the very end of the GUI container, **only select the numbers** anything else will make the bot get confused so try to only select the score position.
+ When you're done, you will notice a green box appear whenever you drag the mouse, if you did not select the correct area or you selected more than one area, you have to take another screenshot, else the bot will get confused. You will only need to do this process once per bot instance.
+ After you're done, press the **"Q"** key in your keyboard and then the bot will start.
+ Quickly, press **"Space"** and click on the **"Restart Game"** button for the minigame to go back to the start screen.
+ Leave the computer alone for the time the bot will run.
+ If you want to cancel the process, press the **"0"** numpad/number key in your keyboard or close the bot's console window and the bot will cease any activity.

<p align="center">
  <img src="https://raw.githubusercontent.com/Unovamata/Make-Some-Noise-Bot/main/Wiki/Window Tutorial 3.png" />
</p>

Have fun!
