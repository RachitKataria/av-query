from __future__ import division
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sys

#Loading audio files
audio_files = np.array(["sports", "movie", "interview", "StarCraft", "musicvideo", "flowers", "traffic"])

# Get query video from command line 
query_file = sys.argv[1]
yQuery, srQuery = librosa.load('query/' + query_file)

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
	yWav, srWav = librosa.load('wav/' + file + '.wav')

	# Starting point for slice
	starting_point = 0

	# Ending point for final slice
	ending_point = len(yWav) - len(yQuery)
	# print("Ending point: ", ending_point)

	min_dist = sys.float_info.max
	min_seconds = 0

	while starting_point <= ending_point:
		# print("Starting sample: ", starting_point)
		# print("Starting second: ", starting_point / srQuery)

		yWavWindow = yWav[starting_point: starting_point + len(yQuery)]

		mfcc1 = librosa.feature.mfcc(yWavWindow, srWav) # Computing MFCC values
		mfcc2 = librosa.feature.mfcc(yQuery, srQuery)

		# Calculate absolute distance
		euclidean_norm = np.linalg.norm(mfcc1.T - mfcc2.T)
		# print(abs_dist)

		if euclidean_norm < min_dist:
			min_dist = euclidean_norm
			min_seconds = starting_point / srQuery

		starting_point += sliding_sample_offset

	print("File name: ", file)
	print("Minimum distance: ", min_dist)
	print("Minimum seconds: ", min_seconds)

	overall_distances.append(min_dist)
	overall_seconds.append(min_seconds)

# Convert to arrays
audio_files = np.asarray(audio_files)
overall_distances = np.asarray(overall_distances)
overall_seconds = np.asarray(overall_seconds)

sorted_indices = np.argsort(overall_distances)
print(audio_files[sorted_indices])
print(overall_distances[sorted_indices])
print(overall_seconds[sorted_indices])
