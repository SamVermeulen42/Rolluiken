import serial, threading, datetime

class SerialController:
  ser = serial.Serial('/dev/ttyAMA0', 2400)
  ser.open()
  lock = threading.Lock()

  @classmethod
  def send(cls, cardNr, command, relayNr):
    checksum = (1024 - 13 - cardNr - ord(command) - 48 - relayNr) & 255
    cls.lock.acquire()
    cls.ser.write('\r' + chr(cardNr) + command + chr(48+relayNr) + chr(checksum))
    cls.ser.write('\r' + chr(cardNr) + command + chr(48+relayNr) + chr(checksum))
    cls.ser.write('\r' + chr(cardNr) + command + chr(48+relayNr) + chr(checksum))
    cls.ser.flush()
    threading.Timer(0.9, cls.lock.release).start()
