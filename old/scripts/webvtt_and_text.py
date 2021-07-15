#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
from webvtt import WebVTT, Caption
import sys
import os
import subprocess
import json
import textwrap

# creates webvtt and text file for the video given

SetLogLevel(-1)

if not os.path.exists('model'):
    print('Please download the model from https://alphacephei.com/vosk/models'
        ' and unpack as `model` in the current folder.')
    exit(1)

sample_rate = 16000
model = Model('model')
rec = KaldiRecognizer(model, sample_rate)
rec.SetWords(True)

WORDS_PER_LINE = 7


def timeString(seconds):
    minutes = seconds / 60
    seconds = seconds % 60
    hours = int(minutes / 60)
    minutes = int(minutes % 60)
    return '%i:%02i:%06.3f' % (hours, minutes, seconds)


def transcribe():
    command = ['ffmpeg', '-nostdin', '-loglevel', 'quiet', '-i', sys.argv[1],
                # use default command here mostly but boost volume by a bit 
                '-ar', str(sample_rate),'-filter:a', 'volume=2', '-ac', '1', '-f', 's16le', '-']
    process = subprocess.Popen(command, stdout=subprocess.PIPE)

    results = []
    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(rec.Result())
    results.append(rec.FinalResult())

    ############# Create webtvv subtitle file ###########
    vtt = WebVTT()
    for i, res in enumerate(results):
        words = json.loads(res).get('result')
        if not words:
            continue

        start = timeString(words[0]['start'])
        end = timeString(words[-1]['end'])
        content = ' '.join([w['word'] for w in words])

        caption = Caption(start, end, textwrap.fill(content))
        vtt.captions.append(caption)

    # save or return webvtt
    if len(sys.argv) > 2:
        vtt.save(sys.argv[2])
    else:
        print(vtt.content)
    
    ############ Save plain text file too as transcript  ###############

    rawText = ''
    for i, res in enumerate(results):
        text = json.loads(res).get('text')
        rawText = rawText + ' ' + text

    if len(sys.argv) > 2:
        with open(sys.argv[2] + ".txt", "w") as file1:
            file1.write(rawText)
    else:
        print(rawText)

if __name__ == '__main__':
    if not (1 < len(sys.argv) < 4):
        print(f'Usage: {sys.argv[0]} audiofile [output file]')
        exit(1)
    transcribe()
