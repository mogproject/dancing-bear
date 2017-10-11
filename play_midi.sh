#!/bin/bash

set -e

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <BPM> <NumberOfBeats>"
    exit 1
fi

bpm=$1
num_beats=$2

# Check input
if (( bpm < 40 || bpm > 300 )); then
    echo 'BPM must be between 40 and 300.'
    exit 2
fi

if (( num_beats < 1 || num_beats > 20 )); then
    echo 'NumberOfBeats must be between 1 and 20.'
    exit 2
fi

wait_sec=$((60000 / ${bpm} / 1000))
wait_ms=$((60000 / ${bpm} % 1000))

# Identify the device
device=$(sendmidi list | head -1)

if [[ "$device" = "" ]]; then
    echo 'No MIDI device available.'
    exit 3
fi

# Pan to the center
sendmidi dev "$device" ch 10 cc 10 127

# Play loop
while true; do
    for (( i=1; i<=${num_beats}; ++i )); do
        if [[ i -eq 1 ]]; then
            n=81
        else
            n=80
        fi
        sendmidi dev "$device" ch 10 on ${n} 127
        sleep "${wait_sec}.${wait_ms}"
    done
done
exit 0

