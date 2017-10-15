import serial
import time


class BearController(object):
    def __init__(self, port='/dev/cu.usbmodem1451', baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(port, baud_rate, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
        time.sleep(2)

    def play_downbeat(self):
        self.ser.write(bytearray([0]))

    def play_upbeat(self):
        self.ser.write(bytearray([1]))

    def send_bpm(self, bpm):
        self.ser.write(bytearray([bpm]))
