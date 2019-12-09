import os
import ffmpeg
from app import app
from flask import request, jsonify
from audio.mfcc import mfcc
from edge_detection import detect
from color import histogram_comparison
from color import rgb_to_png

QUERY_FOLDER = os.path.join(app.root_path, '../audio/mfcc/data')

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/audio', methods=['POST'])
def audio():
    if request.method == 'POST':
        print(request.__dict__)
        # Get file name and file path
        filename = request.get_json()['filename']
        file_path = os.path.join(app.root_path, '../audio/mfcc/query', filename)
        # Retrieve ranked wavs for query
        wav_scores = mfcc.get_wavs_scores_for_query(file_path)
        return jsonify(wav_scores)

@app.route('/convert_to_mp4', methods=['POST'])
def convert_to_mp4():
    if request.method == 'POST':
        # Get query directory and file path
        filename = request.get_json()['filename']
        file_path = os.path.join(app.root_path, '../data/query', filename)
        dest_path = os.path.join(app.root_path, '../data/query', filename+"_png")
        rgb_to_png.convert(file_path, dest_path)
        dest_path += "/*.png"
        ffmpeg.input(dest_path, pattern_type='glob', framerate=30).output('query.mp4').overwrite_output().run()
        return jsonify({})

@app.route('/color', methods=['POST'])
def color():
    if request.method == 'POST':
        return jsonify(
            histogram_comparison.get_matches(
                os.path.join(app.root_path, '../data/query', request.get_json()['filename']),
            ),
        )   

@app.route('/edge_detection', methods=['POST'])
def edge_detection():
    if request.method == 'POST':
        return jsonify(
            detect.online_processing(
                os.path.join(app.root_path, request.get_json()['filename']),
            ),
        )
