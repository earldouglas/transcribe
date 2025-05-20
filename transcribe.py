#!/usr/bin/env python3

from json import loads
from pasimple import PA_SAMPLE_S16LE
from pasimple import PA_STREAM_RECORD
from pasimple import PaSimple
from pasimple import format2width
from sys import argv
from sys import exit
from vosk import KaldiRecognizer
from vosk import Model
from vosk import SetLogLevel

SOURCES_COUNT = len(argv) - 1

if not SOURCES_COUNT > 0:
    exit('Usage: transcribe <source0> [source1] ... [sourceN]')

sources = argv[1:]

SetLogLevel(-1)

FORMAT = PA_SAMPLE_S16LE
SAMPLE_WIDTH = format2width(FORMAT)
CHANNELS = 1
SAMPLE_RATE = 48000


def new_pasimple(device_name):
    return PaSimple(
        PA_STREAM_RECORD,
        FORMAT,
        CHANNELS,
        SAMPLE_RATE,
        device_name=device_name
    )


model = Model(lang="en-us")


def new_recognizer():
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    recognizer.SetWords(True)
    recognizer.SetPartialWords(True)
    return recognizer


streams = list(map(new_pasimple, sources))
recognizers = list(map(lambda _: new_recognizer(), streams))


def read_stream(stream):
    return bytes(stream.read(CHANNELS * SAMPLE_RATE * SAMPLE_WIDTH))


try:
    while True:
        byteses = list(map(read_stream, streams))

        for idx in range(SOURCES_COUNT):
            recognizer = recognizers[idx]
            data = byteses[idx]

            if recognizer.AcceptWaveform(data):
                text = loads(recognizer.Result())["text"]
                if len(text) > 0:
                    print('<ch{}> {}'.format(idx, text), flush=True)

except KeyboardInterrupt:
    ()
