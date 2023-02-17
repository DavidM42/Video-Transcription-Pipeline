#!/usr/bin/env python3
import whisper
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

tool = language_tool_python.LanguageTool('de-DE')

sample_rate = 16000
model = whisper.load_model("small")

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

    result = model.transcribe(f'{videoPath}/{fileName}.mp4')

    ############ Save plain text file too as transcript  ###############

    rawText = result["text"]

    with open(f'{transcriptionsPath}/{fileName}-[raw-asr].txt', "w") as file1:
        file1.write(rawText)


    ############  Languagetool correct ###############
    # TODO only use rules that are whitelistet about upper/lowercase
    # see https://community.languagetool.org/rule/list?offset=0&max=10&lang=de&filter=&categoryFilter=Gro%C3%9F-%2FKleinschreibung&_action_list=Filter for that
    matches = tool.check(rawText)
    punctuated_and_corrected = tool.correct(rawText)

    with open(f'{transcriptionsPath}/{fileName}-[grammar-corrected].txt', "w") as file1:
        file1.write(punctuated_and_corrected)

    ############# Create webtvv subtitle file ###########
    vtt = WebVTT()
    for i, res in enumerate(result["segments"]):
        start = timeString(res['start'])
        end = timeString(res['end'])
        content = res["text"]

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

if __name__ == '__main__':
    loop_all_videos()

    # quicker test call then full workflow
    # transcribe('2_2[1]')
