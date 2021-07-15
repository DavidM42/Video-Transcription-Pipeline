# Video Transcription Pipeline (Vosk, Punctuator2, Languagetool)

This project is a quick video transcription pipeline for me to use in university.
Input a folder of videos and get out transcriptions with medium quality and additionally punctuations and grammar checking done.
Pipeline script file can be easily edited to grammar check subtitles output or other adaptions.
A focus was easy and working setup as opposed to [some projects](https://github.com/uhh-lt/subtitle2go) I got inspired by while developing this and struggled to set up.

## Setup (Linux)

### Python environment setup

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r ./requirements.txt
```

### Download German vosk model

```bash
wget https://alphacephei.com/vosk/models/vosk-model-de-0.6.zip
unzip vosk-model-de-0.6.zip
mv vosk-model-de-0.6 voskModel
```

### Download German punctuator2 model

```bash
cd punctuatorModel
wget http://ltdata1.informatik.uni-hamburg.de/subtitle2go/Model_subs_norm1_filt_5M_tageschau_euparl_h256_lr0.02.pcl
cd ..
```

## Execute

After running the setup and placing all your videos in the video folder run

```bash
source venv/bin/activate
python pipeline.py
```

## Contributions

Thanks to the [Language Technology Group, Universität Hamburg (UHH)](https://github.com/uhh-lt) for providing the used punctuator2 model.
