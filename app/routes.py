import os
from app import app
from flask import request, jsonify
from audio.mfcc import mfcc
from edge_detection import detect

QUERY_FOLDER = os.path.join(app.root_path, '../audio/mfcc/data')

@app.route('/')
@app.route('/index')
def index():
	return "Hello, World!"

@app.route('/audio', methods=['POST'])
def audio():
	if request.method == 'POST':
		# Get file name and file path
		filename = request.get_json()['filename']
		file_path = os.path.join(app.root_path, '../audio/mfcc/query', filename)
		# Retrieve ranked wavs for query
		wav_scores = mfcc.get_wavs_scores_for_query(file_path)
		return jsonify(scores=wav_scores)

@app.route('/edge_detection', methods=['POST'])
def edge_detection():
	if request.method == 'POST':
		return jsonify(
			detect.online_processing(
				os.path.join(app.root_path, request.get_json()['filename']),
			),
		)
