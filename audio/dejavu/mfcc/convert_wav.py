from __future__ import division
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sys
import json

#Loading audio files
audio_files = np.array(["sports", "movie", "interview", "StarCraft", "musicvideo", "flowers", "traffic"])

for file in audio_files:
	# Load in samples and sample rate
	yQuery, srQuery = librosa.load('wav/' + file + '.wav')

	# Save JSON of datums
	file_data = {}
	file_data['data'] = yQuery.tolist()
	file_data['sample_rate'] = srQuery

	with open('data/' + file + '.json', 'w') as audio_json:
		json.dump(file_data, audio_json)