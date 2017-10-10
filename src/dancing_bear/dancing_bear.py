import sys
import time
from datetime import datetime
import signal

from mog_commons.terminal import TerminalHandler
from .bear_controller import BearController

MAX_BPM = 300

def main():
    """
    Main function
    """

    t = TerminalHandler(getch_repeat_threshold=0.05)
    signal.signal(signal.SIGTERM, t.restore_terminal)
    try:
        t.clear()
        print('\n'.join([
            'Usage:',
            '[k]: Start and finish the beat',
            '[j]: Record inner beats',
            '[q]: Quit this program',
            '',
        ]))

        tm = None
        count = 0
        ts = []
        bpm = 0
        num_beats = 0
        while True:
            ch = t.getch()
            tt = datetime.now()

            if ch == 'k':
                if (count < 1):
                    t.clear()
                    print('1')
                    count = 1
                    ts.clear()
                else:
                    ts.append((tt - tm).total_seconds())

                    # check if valid
                    average_elapsed = sum(ts) / len(ts)
                    bpm = round(60 / average_elapsed)

                    if any(map(lambda x:  abs(1 -  x / average_elapsed) > 0.2, ts)):
                        # not constant beat
                        t.clear()
                        print('Beats are not constant. Please retry.')
                        count = 0
                    elif (bpm > MAX_BPM):
                        # bpm too high
                        t.clear()
                        print('BPM too high: %d (Max: %d)' % (bpm, MAX_BPM))
                        count = 0
                    else:
                        bpm = round(60 / average_elapsed)
                        num_beats = len(ts)
                        print('BPM: %d, #Beats: %d' % (bpm, num_beats))
                        break
            elif ch == 'j' and count:
                count += 1
                print(count)
                ts.append((tt - tm).total_seconds())

            if ch == 'q':
                break
            tm = tt
        
        # play sound
        controller = BearController()

        while True:
            for i in range(num_beats):
                controller.flash_led()
                time.sleep(60 / bpm)

        while True:
            ch = t.getch()
            if ch == 'q':
                break

    finally:
        t.restore_terminal(None, None)

def play_sound(bpm, num_beats):
    # todo
    pass