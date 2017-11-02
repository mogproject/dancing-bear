import signal

from mog_commons.terminal import TerminalHandler
from .bear_controller import BearController
from .midi_controller import MidiController
from .bpm_recorder import BPMRecorder


def main():
    """
    Main function
    """
    t = TerminalHandler(getch_repeat_threshold=0.05, keep_input_clean=False)
    signal.signal(signal.SIGTERM, t.restore_terminal)
    try:
        mc = None
        bc = None

        try:
            mc = MidiController()
        except Exception:
            pass

        try:
            bc = BearController()
        except Exception:
            pass

        rec = BPMRecorder(t, mc, bc)
        rec.loop()
    finally:
        t.restore_terminal(None, None)
