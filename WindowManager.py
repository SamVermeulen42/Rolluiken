import threading, time, datetime
from SerialController import SerialController

class WindowManager:

  def __init__(self):
    self.sema = threading.BoundedSemaphore()
    SerialController.send(1,'C',9)
    SerialController.send(2,'C',9)
  
  def execute(self, windowScreen, targetState):
    fromState = windowScreen.state
    windowScreen.state = targetState
    self.sema.acquire()
    if targetState != fromState:
      card = windowScreen.cardClose
      relay = windowScreen.relayClose
      if fromState < targetState:
        # closing
        time = (targetState - fromState) * windowScreen.stepTimeDown
        if targetState == 100:
          time += windowScreen.fullCycleBonus
      else:
        card = windowScreen.cardOpen
        relay = windowScreen.relayOpen
        # opening
        time = (fromState - targetState) * windowScreen.stepTimeUp
        if targetState == 0:
          time += windowScreen.fullCycleBonus
      SerialController.send(card, 'S', relay)
      threading.Timer(time/float(1000), self.stopOutput, [card, relay]).start()
    else:
      self.sema.release()

  def stopOutput(self, card, relay):
    SerialController.send(card, 'C', relay)
    time.sleep(1.5)
    self.sema.release()
  
