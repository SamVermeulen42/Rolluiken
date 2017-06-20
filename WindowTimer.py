import threading, datetime, json

class WindowTimer:
  def runTimer(self):
    self.windowList.windowManager.execute(self.windowScreen, self.targetState)
    day = datetime.datetime.today().weekday()
    self.setDateTime += datetime.timedelta(days = self.shift[day])
    diff = self.setDateTime - datetime.datetime.now()
    self.timer = threading.Timer(diff.seconds, self.runTimer, [])
    self.timer.start()
    self.windowList.saveJSON('/home/pi/rolluiken/init.bak')

  def __init__(self, windowList, description, windowScreen, targetState, hour, minutes, days):
    self.description = description
    self.targetState = targetState
    self.windowScreen = windowScreen
    self.windowList = windowList
    self.hour = hour
    self.minutes = minutes
    self.days = days
    windowScreen.addTimer(self)
    self.renew()

  # starts the initial timer based on set parameters
  def renew(self):
    if len(self.days) != 7 or self.days == [0,0,0,0,0,0,0]:
      raise ValueError('Date argument not correct')
    self.setTime = datetime.time(self.hour, self.minutes)
    self.generateShift()  
    day = datetime.datetime.today().weekday()
    self.setDateTime = datetime.datetime.combine(datetime.date.today(), self.setTime)
    if not (datetime.datetime.now().time() < self.setTime and self.days[day]):
      self.setDateTime += datetime.timedelta(days = self.shift[day])
    diff = self.setDateTime - datetime.datetime.now()
    self.timer = threading.Timer(diff.seconds, self.runTimer, [])
    self.timer.start()

  def generateShift(self):
    placed = 0
    self.shift = [0,0,0,0,0,0,0]
    for i in range(0,7):
      if self.days[(i+1) % 7]:
        self.shift[i] = 1
        placed += 1
    while placed < 7:
      for i in range(6,-1,-1):
        if self.shift[i] == 0 and self.shift[(i+1)%7] != 0:
          self.shift[i] = self.shift[(i+1)%7] + 1
          placed += 1

  def removeTimer(self):
    self.timer.cancel() 
