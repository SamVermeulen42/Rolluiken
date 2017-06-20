from WindowManager import WindowManager
from WindowScreen import WindowScreen
from WindowTimer import WindowTimer
import json 

class WindowList:

  def __init__(self):
    self.windowManager = WindowManager()
    self.windowScreens = [] 
    
  def readJSON(self, filename):
    raw = open(filename)
    data = json.load(raw)
    for i in data['windows']:
      window = WindowScreen(i['name'],
          i['state'],
          i['cardOpen'],
          i['relayOpen'],
          i['cardClose'],
          i['relayClose'],
          i['stepTimeUp'],
          i['stepTimeDown'],
          i['fullCycleBonus'],
          i['openLight'],
          i['closeLight'],
          i['closeState'])
      for j in i['timers']:
        WindowTimer(self, j['description'], window, j['targetState'], j['hour'], j['minutes'], j['days'])
      self.windowScreens.append(window)
    raw.close()

  def saveJSON(self, filename):
    windows = {"windows": []}
    for i in self.windowScreens:
      window = {"name": i.name,
          "state": i.state,
          "cardOpen": i.cardOpen,
          "relayOpen": i.relayOpen,
          "cardClose": i.cardClose,
          "relayClose": i.relayClose,
          "stepTimeUp": i.stepTimeUp,
          "stepTimeDown": i.stepTimeDown,
          "fullCycleBonus": i.fullCycleBonus, 
          "openLight": i.openLight,
          "closeLight": i.closeLight,
          "closeState": i.closeState,
          "timers": []}
      for j in i.timers:
	timer = {"description": j.description, "targetState": j.targetState, "hour": j.hour, "minutes": j.minutes, "days": j.days}
        window['timers'].append(timer)
      windows['windows'].append(window)
    with open(filename, 'w') as out:
      json.dump(windows, out, sort_keys=True, indent=4)

  
