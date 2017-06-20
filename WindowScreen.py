class WindowScreen:
  # name = identifier
  # state 0 = open, 100 = closed
  # stepTime = time for a single percentage (0 <-> 1) in ms
  # fullCycleBonus = time to add to a full run (up to 0 or 100)
  # timers = list of timers

  def __init__(self, name, state, cardOpen, relayOpen, cardClose, relayClose, stepTimeUp, stepTimeDown, fullCycleBonus, openLight, closeLight, closeState):
    self.name = name
    self.state = state
    self.cardOpen = cardOpen
    self.relayOpen = relayOpen
    self.cardClose = cardClose
    self.relayClose = relayClose
    self.stepTimeUp = stepTimeUp
    self.stepTimeDown = stepTimeDown
    self.fullCycleBonus = fullCycleBonus
    self.openLight = openLight
    self.closeLight = closeLight
    self.closeState = closeState
    self.timers = []

  def addTimer(self, timer):
    self.timers.append(timer)
