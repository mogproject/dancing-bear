from mog_commons.command import execute_command, capture_command
import os
import signal
import subprocess


class MidiController:
    CH_DRUMS = 10
    NOTE_DOWNBEAT = 81
    NOTE_UPBEAT = 80
    NOTE_VELOCITY = 127

    def __init__(self, port='SimpleSynth virtual input'):
        self.port = port

        # check deivce
        rc, stdout, stderr = capture_command(['sendmidi', 'list'])
        if port not in str(stdout, 'utf-8').splitlines(False):
            raise RuntimeError('MIDI device not found.')

        xs = ['sendmidi', 'dev', self.port, 'ch', MidiController.CH_DRUMS, 'on']
        self.downbeat_args = xs + [MidiController.NOTE_DOWNBEAT, MidiController.NOTE_VELOCITY]
        self.upbeat_args = xs + [MidiController.NOTE_UPBEAT, MidiController.NOTE_VELOCITY]
        self.midi_pid = None

    def play_downbeat(self):
        execute_command(self.downbeat_args)

    def play_upbeat(self):
        execute_command(self.upbeat_args)

    def start_play(self, bpm, num_beats):
        args = ['./play_midi.sh', str(bpm), str(num_beats)]
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False, preexec_fn=os.setsid)
        self.midi_pid = proc.pid

    def stop_play(self):
        if (self.midi_pid is not None):
            try:
                os.killpg(os.getpgid(self.midi_pid), signal.SIGTERM)
            except Exception:
                pass
            self.midi_pid = None
