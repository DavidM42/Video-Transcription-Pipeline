# Video Transcription Pipeline (Whisper, Languagetool, supports german)

This project is a quick video transcription pipeline for me (and you) to use in university.
Input a folder of videos and get out transcriptions (plus subtitle files) with additional grammar checking done.
Pipeline script file can be easily edited to grammar check subtitles too, output different formats or other adaptions.
A focus was easy and working setup as opposed to [some projects](https://github.com/uhh-lt/subtitle2go) I got inspired by while developing this and struggled to set up.

The current second version of this tool utilizes the advanced speech recognition model called [**whisper**](https://github.com/openai/whisper) built by OpenAI.

## Setup (Linux)

### Download

Clone the repo:

```bash
git clone https://github.com/DavidM42/Video-Transcription-Pipeline.git
```

### Python environment setup

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r ./requirements.txt
```

## Execute

After running the setup and placing all your videos in the video folder run

```bash
source venv/bin/activate
python pipeline.py
```

