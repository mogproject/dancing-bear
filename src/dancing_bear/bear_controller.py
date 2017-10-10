import serial


class BearController(object):
    def __init__(self, port='/dev/cu.usbmodem1451', baud_rate=9600):
        self.ser = serial.Serial(port, baud_rate)

    def flash_led(self):
        self.ser.write(b'1')
