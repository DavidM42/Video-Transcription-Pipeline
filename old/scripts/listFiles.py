from os import listdir
from os.path import isfile, join

videoPath = './videos'

filesWithExtensions = [f for f in listdir(videoPath) if isfile(join(videoPath, f))]
allFilesNoExtensions = [e.replace('.mp4', '') for e in filesWithExtensions]

print(allFilesNoExtensions)
