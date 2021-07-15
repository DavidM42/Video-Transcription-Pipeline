# Instructions

```bash
pip install vosk
# models on https://alphacephei.com/vosk/models
# this model had fairly bad accuarcy for me sadly but make do
wget https://alphacephei.com/vosk/models/vosk-model-de-0.6.zip
unzip vosk-model-de-0.6.zip
mv vosk-model-de-0.6 voskModel
```

Install requirements `pip install -r ./requirements.txt`

## How I got the vosk code

```bash
git clone https://github.com/alphacep/vosk-api
cd vosk-api/python/example
```