import RPi.GPIO as GPIO
import threading, datetime, time

class WindowSensorManager:

  def __init__(self, windowList):
    self.windowList = windowList
    self.windowManager = windowList.windowManager
    self.openEarly = datetime.time(6, 40)
    self.openLate = datetime.time(12, 0)
    self.closeEarly = datetime.time(16, 0)
    self.closeLate = datetime.time(23, 0)
    GPIO.setup(16, GPIO.IN)
    self.dark = GPIO.input(16)
    self.changed()
    t1 = threading.Thread(target = self.listen)
    t1.start()
    
  def listen(self):
    while True:
      value = GPIO.input(16)
      if self.dark != value:
        self.dark = value
        self.changed()
      time.sleep(60)
  
  def changed(self):
    now = datetime.datetime.now().time()
    if self.dark:
      if now < self.closeLate and now > self.closeEarly:
        for windowScreen in self.windowList.windowScreens:
          if windowScreen.closeLight:
            self.windowManager.execute(windowScreen, windowScreen.closeState)
    else:
      if now < self.openLate:
        if now > self.openEarly:
          self.openLight()
        else:
          date = datetime.date.today()
          time = datetime.datetime.combine(date, self.openEarly)
          diff = time - datetime.datetime.now()

          timer = threading.Timer(diff.seconds, self.openLight, [])
          timer.start()
    self.windowList.saveJSON('/home/pi/rolluiken/init.bak')     
      
  def openLight(self):
    for windowScreen in self.windowList.windowScreens:
      if windowScreen.openLight:
        self.windowManager.execute(windowScreen, 0)
    self.windowList.saveJSON('/home/pi/rolluiken/init.bak')



 
