import signal
import sys
from optparse import OptionParser

from mog_commons.terminal import TerminalHandler
from .bear_controller import BearController
from .midi_controller import MidiController
from .bpm_recorder import BPMRecorder
from .gui_controller import GUIController


def main():
    """
    Main function
    """
    t = TerminalHandler(getch_repeat_threshold=0.05, keep_input_clean=False)
    signal.signal(signal.SIGTERM, t.restore_terminal)

    # parse arguments
    options, args = get_parser().parse_args(sys.argv[1:])

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

        gc = GUIController()

        rec = BPMRecorder(t, mc, bc, gc, options.bpm, options.beat)
        rec.loop(options.bpm is not None)
        gc.close()
    finally:
        t.restore_terminal(None, None)


def get_parser():
    """
    Get command line arguments parser
    """
    parser = OptionParser(version="0.0.1", usage="%prog [options]")

    parser.add_option(
        '--bpm', dest='bpm', default=None, type='int',
        help='beats per minute'
    )
    parser.add_option(
        '--beat', dest='beat', default=None, type='int',
        help='number of beats'
    )

    return parser
