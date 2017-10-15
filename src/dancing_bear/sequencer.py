import asyncio
import concurrent
from datetime import timedelta


def start_sequence(bear_controller, midi_controller, bpm, num_beats):
    loop = asyncio.new_event_loop()

    # schedule the first beat
    loop.call_soon(play_beat, loop, bear_controller, midi_controller, loop.time(), bpm, num_beats, 0)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    loop.close()


def play_beat(loop, bear_controller, midi_controller, start_time, bpm, num_beats, beat_count):
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

    # schedule next beat
    c = beat_count + 1
    t = start_time + 60 * (c // bpm) + 60 / bpm * (c % bpm)
    loop.call_at(t, play_beat, loop, bear_controller, midi_controller, start_time, bpm, num_beats, c)
