from datetime import datetime
import sys
import time


class BPMRecorder:
    MAX_BPM = 255
    MIN_BPM = 40

    def __init__(self, term, midi_controller=None, bear_controller=None):
        self.term = term
        self.midi_controller = midi_controller
        self.bear_controller = bear_controller
        self._print_header()

    def loop(self):
        count = 0
        last_recorded = None
        time_recorded = []

        while True:
            ch = self.term.getch()
            current_time = datetime.now()

            if ch == 'k' and count == 0:
                # Start recording
                self._stop_play()

                # initialize
                time_recorded.clear()
                count += 1
                print(count)
                self._play_downbeat()

            elif ch == 'k':
                # Stop recording
                time_recorded.append((current_time - last_recorded).total_seconds())

                # calculate values
                num_beats = len(time_recorded)
                average_elapsed = sum(time_recorded) / num_beats
                bpm = round(60 / average_elapsed)

                # validate
                if any(map(lambda x: abs(1 - x / average_elapsed) > 0.2, time_recorded)):
                    # not constant beat
                    self._print_message('Beats are not constant. Please retry.')
                elif (bpm > BPMRecorder.MAX_BPM):
                    # bpm too high
                    self._print_message('BPM too high: %d (Max: %d). Please retry.' % (bpm, BPMRecorder.MAX_BPM))
                elif (bpm < BPMRecorder.MIN_BPM):
                    # bpm too low
                    self._print_message('BPM too low: %d (Min: %d). Please retry.' % (bpm, BPMRecorder.MIN_BPM))
                else:
                    # ok
                    self._print_message('Playing: BPM=%d, #Beats=%d\n\nPress Ctrl-C to stop.' % (bpm, num_beats))
                    self._start_play(bpm, num_beats)
                count = 0

            elif ch == 'j' and count == 0:
                self._stop_play()
                self._print_header()

            elif ch == 'j':
                # Record upbeats
                time_recorded.append((current_time - last_recorded).total_seconds())

                count += 1
                print(count)
                self._play_upbeat()

            elif ch == 'q':
                self._stop_play()
                break

            last_recorded = current_time

    def _print_header(self):
        self.term.clear()
        print('[Q] Quit   [K] Start/stop recording   [J] Record upbeat\n')

    def _print_message(self, message):
        self._print_header()
        print(message)
        print()

    def _play_downbeat(self):
        if (self.midi_controller is not None):
            self.midi_controller.play_downbeat()
        if (self.bear_controller is not None):
            self.bear_controller.play_downbeat()

    def _play_upbeat(self):
        if (self.midi_controller is not None):
            self.midi_controller.play_upbeat()
        if (self.bear_controller is not None):
            self.bear_controller.play_upbeat()

    def _start_play(self, bpm, num_beats):
        interval = 60 / bpm
        i = 0
        try:
            while True:
                if i == 0:
                    self._play_downbeat()
                else:
                    self._play_upbeat()
                time.sleep(interval)
                i = (i + 1) % num_beats
        except KeyboardInterrupt:
            self._print_header()

    def _stop_play(self):
        if (self.midi_controller is not None):
            self.midi_controller.stop_play()
