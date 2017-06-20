import socket, threading, json, datetime
from WindowList import WindowList
from WindowTimer import WindowTimer

def toBool(s):
    if s == 'true':
      return True
    else:
      return False

class WindowMessageReciever:

  def __init__(self, windowList):
    self.windowList = windowList

  def runReciever(self):
    t1 = threading.Thread(target = self.startReciever)
    t1.start()

  def startReciever(self):
    TCP_IP = '0.0.0.0'
    TCP_PORT = 4993
    BUFFER_SIZE = 20

    s = socket.socket()
    s.bind( (TCP_IP, TCP_PORT) )
    s.listen(20)

    while 1:
      c, addr = s.accept()
      request = c.recv(4096)
      reqList = request.split('%')
      if reqList[0] == 'simple':
        c.send(self.serializeDataSimple())
      elif reqList[0] == 'advanced':
        c.send(self.serializeDataAdvanced(int(reqList[1])))
      elif reqList[0] == 'move':
        threading.Thread(target = self.windowList.windowManager.execute, args = (self.windowList.windowScreens[int(reqList[1])], int(reqList[2]))).start()
        c.send('done')
	self.windowList.saveJSON('/home/pi/rolluiken/init.bak')
      elif reqList[0] == 'set':
	threading.Thread(target = self.parseSetReq, args = (reqList,)).start()
	c.send('done')
      c.close()

  def parseSetReq(self, reqList):
    rolluik = self.windowList.windowScreens[int(reqList[1])]
    for t in rolluik.timers:
      t.removeTimer()
    rolluik.timers = []
    raw = json.loads(reqList[2])
    rolluik.closeState = raw['closeState']
    rolluik.openLight = raw['openLight']
    rolluik.closeLight = raw['closeLight']
    timersjs = raw['timers']
    for t in timersjs:
      timer = WindowTimer(self.windowList, t['description'], rolluik, t['targetState'], t['hour'], t['minutes'], t['days'])
    self.windowList.saveJSON('/home/pi/rolluiken/init.bak')

  def serializeDataSimple(self):
    s = {"windows": []}
    for i in self.windowList.windowScreens:
      window = {"name": i.name, "state": i.state}
      s['windows'].append(window)
    return json.dumps(s)
  
  def serializeDataAdvanced(self, nr):
    i = self.windowList.windowScreens[nr]
    timers = []
    for j in i.timers:
      timer = {"description": j.description, "targetState": j.targetState, "hour": j.hour, "minutes": j.minutes, "days": j.days}
      timers.append(timer)
    window = {"name": i.name, "state": i.state, "openLight": i.openLight, "closeLight": i.closeLight, "closeState": i.closeState, "timers": timers}
    return json.dumps(window)



