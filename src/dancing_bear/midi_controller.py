from mog_commons.command import execute_command

class MidiController:
    CH_DRUMS = 10
    NOTE_DOWNBEAT = 81
    NOTE_UPBEAT = 80
    NOTE_VELOCITY = 127

    def __init__(self, port='SimpleSynth virtual input'):
        self.port = port

    def play_downbeat(self):
        execute_command(['sendmidi', 'dev', self.port, 'ch', MidiController.CH_DRUMS, 'on', MidiController.NOTE_DOWNBEAT, MidiController.NOTE_VELOCITY])
    
    def play_upbeat(self):
        execute_command(['sendmidi', 'dev', self.port, 'ch', MidiController.CH_DRUMS, 'on', MidiController.NOTE_UPBEAT, MidiController.NOTE_VELOCITY])
