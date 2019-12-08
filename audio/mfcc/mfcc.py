from __future__ import division
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sys
import json
import os

DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/')

def get_ranked_wavs_for_query(file_path):
	# Number of ranked files to return
	num_ranked_files = 3

	#Loading audio files
	audio_files = np.array(["sports", "movie", "interview", "StarCraft", "musicvideo", "flowers", "traffic"])
	yQuery, srQuery = librosa.load(file_path)

	# Frames per second
	fps = 30

	# Frames per sliding window
	sliding_window_frames = fps // 2
	samples_per_frame = srQuery // fps
	sliding_sample_offset = samples_per_frame * sliding_window_frames 

	# Overall min distances and seconds
	overall_distances = []
	overall_seconds = []

	for file in audio_files:
		with open(DATA_FOLDER + file + '.json') as audio_json:
			data = json.load(audio_json)

			# Get data and sample rate
			yWav = np.asarray(data['data'])
			srWav = data['sample_rate']

			# Starting point for slice
			starting_point = 0

			# Ending point for final slice
			ending_point = len(yWav) - len(yQuery)

			min_dist = sys.float_info.max
			min_seconds = 0

			while starting_point <= ending_point:
				yWavWindow = yWav[starting_point: starting_point + len(yQuery)]

				mfcc1 = librosa.feature.mfcc(yWavWindow, srWav) # Computing MFCC values
				mfcc2 = librosa.feature.mfcc(yQuery, srQuery)

				# Calculate euclidean distance
				euclidean_norm = np.linalg.norm(mfcc1.T - mfcc2.T)

				if euclidean_norm < min_dist:
					min_dist = euclidean_norm
					min_seconds = starting_point / srQuery

				starting_point += sliding_sample_offset

			# print("File name: ", file)
			# print("Minimum distance: ", min_dist)
			# print("Minimum seconds: ", min_seconds)

			overall_distances.append(min_dist)
			overall_seconds.append(min_seconds)

	# Convert to arrays
	audio_files = np.asarray(audio_files)
	overall_distances = np.asarray(overall_distances)
	overall_seconds = np.asarray(overall_seconds)
	sorted_indices = np.argsort(overall_distances)

	# # New line
	# print('\n')
	# print("Ranked List of Matches")
	# print(audio_files[sorted_indices][:num_ranked_files])
	# print(overall_distances[sorted_indices][:num_ranked_files])
	# print(overall_seconds[sorted_indices][:num_ranked_files])

	return audio_files[sorted_indices][:num_ranked_files], overall_distances[sorted_indices][:num_ranked_files], overall_seconds[sorted_indices][:num_ranked_files]
