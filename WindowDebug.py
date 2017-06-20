import datetime
import os
import shutil

class WindowDebug:
  i = 0
  f = open('/home/pi/rolluiken/debug' + (i+1) + '.txt', 'r+')
  f.truncate()
  
  @classmethod
  def log(cls, text):
    
