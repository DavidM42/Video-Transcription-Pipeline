# Instructions

Generally from https://github.com/uhh-lt/subtitle2go install readme

```bash
git clone https://github.com/ottokart/punctuator2.git
```

- Install requirements `pip install -r ./requirements.txt`
- Patch punctuator2:
  - Open punctuator2/models.py in a file editor, go to line 54 and replace "from . import models" with "import models"

- Download and place model

```bash
mkdir punctuatorModel
cd punctuatorModel
# from https://github.com/uhh-lt/subtitle2go/blob/master/download_models.sh
wget http://ltdata1.informatik.uni-hamburg.de/subtitle2go/Model_subs_norm1_filt_5M_tageschau_euparl_h256_lr0.02.pcl
cd ..
```