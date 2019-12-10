import os
import ffmpeg
import imageio
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
        # Get file name and file path
        filename = request.get_json()['filename']
        file_path = os.path.join(app.root_path, '../data/query', filename)
        # Retrieve ranked wavs for query
        return jsonify(mfcc.get_wavs_scores_for_query(file_path))

@app.route('/convert_to_mp4', methods=['POST'])
def convert_to_mp4():
    if request.method == 'POST':
        # Get query directory
        filename = request.get_json()['filename']
        file_path = os.path.join(app.root_path, '../data/query', filename)
        read_video = rgb_to_png.read_video(file_path)
        imageio.mimwrite(f'{file_path}/{filename}NoAudio.mp4', read_video, fps=30)
        video = ffmpeg.input(f'{file_path}/{filename}NoAudio.mp4')
        audio = ffmpeg.input(f'{file_path}/{filename}.wav')
        ffmpeg.output(video, audio, f'{file_path}/{filename}.mp4').overwrite_output().run()
        os.remove(f'{file_path}/{filename}NoAudio.mp4')
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
