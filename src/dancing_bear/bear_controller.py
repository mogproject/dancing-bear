import serial


class BearController(object):
    def __init__(self, port='/dev/cu.usbmodem1451', baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(port, baud_rate, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

    def start(self, bpm, num_beats):
        self.ser.write(bytearray([bpm, num_beats]))

    def stop(self):
        self.ser.write(bytearray([0, 0]))
