from __future__ import division
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sys
import json
import os

DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/')

# Local wav files
AUDIO_FILES = np.array(["sports", "movie", "interview", "StarCraft", "musicvideo", "flowers", "traffic"])

# Frames per second
FPS = 30

# Frames per sliding window
SLIDING_WINDOW_FRAMES = FPS // 2

def get_wavs_scores_for_query(file_path):
	# Number of ranked files to return
	num_ranked_files = 3

	yQuery, srQuery = librosa.load(file_path)
	
	# Samples per frame and sample offset
	samples_per_frame = srQuery // FPS
	sliding_sample_offset = samples_per_frame * SLIDING_WINDOW_FRAMES 

	# Get MFCC for query once
	mfccQuery = librosa.feature.mfcc(yQuery, srQuery) 

	wav_scores = {}

	for file in AUDIO_FILES:
		with open(DATA_FOLDER + file + '.json') as audio_json:
			data = json.load(audio_json)

			# Get data and sample rate
			yWav = np.asarray(data['data'])
			srWav = data['sample_rate']

			# Starting point for slice
			starting_point = 0

			# Ending point for final slice
			ending_point = len(yWav) - len(yQuery)

			# Create array for wav_scores
			wav_scores[file] = []

			while starting_point <= ending_point:
				yWavWindow = yWav[starting_point: starting_point + len(yQuery)]
 
				# Compute MFCC values for wav file
				mfccWav = librosa.feature.mfcc(yWavWindow, srWav)

				# Calculate euclidean distance
				euclidean_norm = np.linalg.norm(mfccWav - mfccQuery)
				starting_point += sliding_sample_offset

				# Append euclidean norm
				wav_scores[file].append(float(euclidean_norm))

	# Interpolate 2nd to last value as last one
	for file in AUDIO_FILES:
		wav_scores[file].append(wav_scores[file][-1])

	return wav_scores
