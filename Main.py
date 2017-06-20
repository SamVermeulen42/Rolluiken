from WindowList import WindowList
from WindowMessageReciever import WindowMessageReciever
from WindowSensorManager import WindowSensorManager
from SerialController import SerialController
from WindowTimer import WindowTimer
import time

time.sleep(15)

windowList = WindowList()
windowList.readJSON('/home/pi/rolluiken/init.bak')

reciever = WindowMessageReciever(windowList)
reciever.runReciever()

WindowSensorManager = WindowSensorManager(windowList)

# timer = WindowTimer(windowList, 'testDesc', windowList.windowScreens[3], 65, 19, 12, [0, 0, 1, 0, 1, 1, 1])
