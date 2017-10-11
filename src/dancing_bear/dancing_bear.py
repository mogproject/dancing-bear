import sys
import time
import signal

from mog_commons.terminal import TerminalHandler
from .bear_controller import BearController
from .midi_controller import MidiController
from .bpm_recorder import BPMRecorder


def main():
    """
    Main function
    """
    t = TerminalHandler(getch_repeat_threshold=0.05)
    signal.signal(signal.SIGTERM, t.restore_terminal)
    try:
        # rec = BPMRecorder(t, MidiController(), BearController())
        rec = BPMRecorder(t, MidiController(), None)
        rec.loop()
    finally:
        t.restore_terminal(None, None)
