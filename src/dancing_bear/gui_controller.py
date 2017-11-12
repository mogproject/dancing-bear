
class GUIController:
    def __init__(self, data_path='/var/tmp/dancing-bear.dat'):
        self.data = open(data_path, 'wb')
        self.current_beat = 1

    def play_downbeat(self):
        self.current_beat = 1
        self.data.write(bytearray([self.current_beat]))
        self.data.flush()

    def play_upbeat(self):
        self.current_beat += 1
        self.data.write(bytearray([self.current_beat]))
        self.data.flush()

    def send_bpm(self, bpm):
        self.data.write(bytearray([bpm]))

    def close(self):
        self.data.close()
