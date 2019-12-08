import os
from app import app
from flask import request, jsonify
from audio.mfcc import mfcc

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
		audio_files, distances, seconds = mfcc.get_ranked_wavs_for_query(file_path)
		return jsonify(audio_files=audio_files.tolist(), distances=distances.tolist(), seconds=seconds.tolist())
