import asyncio
import concurrent
from datetime import timedelta
import signal
import sys

def start_sequence(bear_controller, midi_controller, gui_controller, bpm, num_beats):
    if bear_controller is not None:
        bear_controller.send_bpm(bpm)

    loop = asyncio.new_event_loop()

    # add sigterm handler
    loop.add_signal_handler(signal.SIGTERM, lambda: loop.stop())

    # schedule the first beat
    loop.call_soon(play_beat, loop, bear_controller, midi_controller, gui_controller, loop.time(), bpm, num_beats, 0)

    try:
        gui_controller.send_bpm(bpm, num_beats)
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    loop.close()


def play_beat(loop, bear_controller, midi_controller, gui_controller, start_time, bpm, num_beats, beat_count):
    is_downbeat = beat_count % num_beats == 0

    if midi_controller is not None:
        if is_downbeat:
            midi_controller.play_downbeat()
        else:
            midi_controller.play_upbeat()
    if bear_controller is not None:
        if is_downbeat:
            bear_controller.play_downbeat()
        else:
            bear_controller.play_upbeat()

    if is_downbeat:
        gui_controller.play_downbeat()
    else:
        gui_controller.play_upbeat()

    # schedule next beat
    c = beat_count + 1
    t = start_time + 60 * (c // bpm) + 60 / bpm * (c % bpm)
    loop.call_at(t, play_beat, loop, bear_controller, midi_controller, gui_controller, start_time, bpm, num_beats, c)
