#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
from webvtt import WebVTT, Caption
import sys
import os
import subprocess
import json
import textwrap

from os import listdir
from os.path import isfile, join

import language_tool_python

# all the used paths
videoPath = './videos'
transcriptionsPath = './transcriptions'
tmp_punctuate_path = './punctuated.txt'

tool = language_tool_python.LanguageTool('de-DE')

SetLogLevel(-1)

if not os.path.exists('voskModel'):
    print('Please follow the voskSetupInstruction.md file in this repo to install vosk.')
    exit(1)

if not os.path.exists('punctuatorModel'):
    print('Please follow the punctuator2SetupInstruction.md file in this repo to install punctuator2.')
    exit(1)

sample_rate = 16000
model = Model('voskModel')
rec = KaldiRecognizer(model, sample_rate)
rec.SetWords(True)

WORDS_PER_LINE = 7


def timeString(seconds):
    minutes = seconds / 60
    seconds = seconds % 60
    hours = int(minutes / 60)
    minutes = int(minutes % 60)
    return '%i:%02i:%06.3f' % (hours, minutes, seconds)


def list_files_in_video_dir():
    filesWithExtensions = [f for f in listdir(videoPath) if isfile(join(videoPath, f))]
    return [e.replace('.mp4', '') for e in filesWithExtensions]

def transcribe(fileName):
    print(f'Transcribing file {videoPath}/{fileName}.mp4...')

    command = ['ffmpeg', '-nostdin', '-loglevel', 'quiet', '-i', f'{videoPath}/{fileName}.mp4' ,
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

    ############ Save plain text file too as transcript  ###############

    rawText = ''
    for i, res in enumerate(results):
        text = json.loads(res).get('text')
        rawText = rawText + ' ' + text

    with open(f'{transcriptionsPath}/{fileName}-[raw-asr].txt', "w") as file1:
        file1.write(rawText)

    # punctuate
    command = f'echo "{rawText}" | python punctuator2/punctuator.py punctuatorModel/Model_subs_norm1_filt_5M_tageschau_euparl_h256_lr0.02.pcl "{tmp_punctuate_path}"'
    os.system(command)
    punctuated_readable_path = f'{transcriptionsPath}/{fileName}-[punctuated].txt'
    second_command = f'python punctuator2/convert_to_readable.py "{tmp_punctuate_path}" "{punctuated_readable_path}"'
    os.system(second_command)

    # correct by reading punctuated, finding matches then apply correction
    with open(punctuated_readable_path, "r") as puncutatedTmpFile:
        punctuated = puncutatedTmpFile.read()
    matches = tool.check(punctuated)
    punctuated_and_corrected = tool.correct(punctuated)

    with open(f'{transcriptionsPath}/{fileName}-[punctuated-grammar-corrected].txt', "w") as file1:
        file1.write(punctuated_and_corrected)

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

    # save webvtt
    vtt.save(f'{transcriptionsPath}/{fileName}')


def loop_all_videos():
    fileNames = list_files_in_video_dir()
    print("Video files:")
    print(fileNames)

    for name in fileNames:
        transcribe(name)

    # remove temp files
    os.remove(tmp_punctuate_path) 


if __name__ == '__main__':
    loop_all_videos()

    # quicker test call then full workflow
    # transcribe('2_2[1]')
