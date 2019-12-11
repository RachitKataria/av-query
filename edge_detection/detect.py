import cv2
import glob
import json
import numpy as np
import os
import shutil
import sys
from PIL import Image

CACHE = './edge_detection/cache'
EDGES = './edge_detection/edges'
VIDEO_DB = './data/database_videos'
VIDEO_DB_FRAMES = 600
VIDEO_QUERY_FRAMES = 150
VIDEO_WIDTH = 352
VIDEO_HEIGHT = 288
VIDEO_CHANNELS = 3
CANNY_SIGMA = 0.15


def fast_load_video(path, videos, video_idx):
    print(f'Loading video from {path} into idx={video_idx} in videos')
    frames = glob.glob(f'{path}/*.rgb')
    frames.sort()
    for frame_idx, frame in enumerate(frames):
        with open(frame, 'rb') as file:
            r = np.asarray(
                Image.frombytes('L', (VIDEO_WIDTH, VIDEO_HEIGHT), file.read(VIDEO_WIDTH * VIDEO_HEIGHT), 'raw'),
                dtype=np.uint8)
            g = np.asarray(
                Image.frombytes('L', (VIDEO_WIDTH, VIDEO_HEIGHT), file.read(VIDEO_WIDTH * VIDEO_HEIGHT), 'raw'),
                dtype=np.uint8)
            b = np.asarray(
                Image.frombytes('L', (VIDEO_WIDTH, VIDEO_HEIGHT), file.read(VIDEO_WIDTH * VIDEO_HEIGHT), 'raw'),
                dtype=np.uint8)
            videos[video_idx][frame_idx] = np.stack((r, g, b), axis=-1)


def fast_load_db(path):
    print(f'Loading database from {path}')

    # Load from cache if exists
    if os.path.exists(f'{CACHE}/video_to_index.json') and os.path.exists(f'{CACHE}/videos.npy'):
        with open(f'{CACHE}/video_to_index.json') as file:
            video_to_index = json.load(file)
        videos = np.load(f'{CACHE}/videos.npy')
        print(f'Finished loading database [CACHE]')
        return videos, video_to_index

    # Nothing from cache, load from disk
    num_videos = sum(os.path.isdir(f'{path}/{vp}') if vp[0] != '.' else 0 for vp in os.listdir(path))
    videos = np.zeros((num_videos, VIDEO_DB_FRAMES, VIDEO_HEIGHT, VIDEO_WIDTH, VIDEO_CHANNELS), dtype=np.uint8)

    video_to_index, idx = {}, 0
    for vp in os.listdir(path):
        if vp[0] != '.':
            fast_load_video(f'{path}/{vp}', videos, idx)
            video_to_index[vp] = idx
            idx += 1

    # Save to cache
    with open(f'{CACHE}/video_to_index.json', 'w') as file:
        json.dump(video_to_index, file)
    np.save(f'{CACHE}/videos', videos)

    print(f'Finished loading database [DISK]')
    return videos, video_to_index


def offline_processing_canny_edge_detection(videos, video_to_index, sigma=CANNY_SIGMA, visualize=False):
    # Delete existing edges folder if exists
    if os.path.exists(EDGES) and os.path.isdir(EDGES):
        shutil.rmtree(EDGES)
    os.mkdir(EDGES)

    # Create edge array of same shape and type as videos, except that it
    # will not maintain channels b/c of the conversion to grayscale during
    # Canny Edge Detection
    edges = np.zeros(videos.shape[0:videos.ndim - 1], dtype=np.int16)

    for k, v in video_to_index.items():
        # k: Video Name, v: Index in videos
        print(f'Detecting edges in video {k}')

        if visualize:
            os.mkdir(f'{EDGES}/{k}')

        for frame in range(VIDEO_DB_FRAMES):
            # Perform pre-steps (RGB->GRAY, Gaussian Blur)
            gray = cv2.cvtColor(videos[v][frame], cv2.COLOR_RGB2GRAY)
            blur = cv2.GaussianBlur(gray, (3, 3), 0)

            # Stats
            median = np.median(blur)
            lower = int(max(0.0, (1.0 - sigma) * median))
            upper = int(min(255.0, (1.0 + sigma) * median))

            # Canny Edge Detection
            edges[v][frame] = cv2.Canny(
                blur,
                lower,
                upper,
            )

            if visualize:
                cv2.imwrite(f'{EDGES}/{k}/{frame}.jpg', edges[v][frame])

    np.save(f'{EDGES}/edges', edges)


def load_canny_edges():
    with open(f'{CACHE}/video_to_index.json') as file:
        video_to_index = json.load(file)
    edges = np.load(f'{EDGES}/edges.npy')
    return edges, video_to_index


def load_query_edges(query_path, sigma=CANNY_SIGMA, visualize=False):
    query_frames = glob.glob(f'{query_path}/*.rgb')
    query_frames.sort()
    query_edges = np.zeros((VIDEO_QUERY_FRAMES, VIDEO_HEIGHT, VIDEO_WIDTH), dtype=np.int16)
    for query_frame_idx, query_frame in enumerate(query_frames):
        with open(query_frame, 'rb') as file:
            r = np.asarray(
                Image.frombytes('L', (VIDEO_WIDTH, VIDEO_HEIGHT), file.read(VIDEO_WIDTH * VIDEO_HEIGHT), 'raw'),
                dtype=np.uint8)
            g = np.asarray(
                Image.frombytes('L', (VIDEO_WIDTH, VIDEO_HEIGHT), file.read(VIDEO_WIDTH * VIDEO_HEIGHT), 'raw'),
                dtype=np.uint8)
            b = np.asarray(
                Image.frombytes('L', (VIDEO_WIDTH, VIDEO_HEIGHT), file.read(VIDEO_WIDTH * VIDEO_HEIGHT), 'raw'),
                dtype=np.uint8)
            gray = cv2.cvtColor(np.stack((r, g, b), axis=-1), cv2.COLOR_RGB2GRAY)
            blur = cv2.GaussianBlur(gray, (3, 3), 0)

            # Stats
            median = np.median(blur)
            lower = int(max(0.0, (1.0 - sigma) * median))
            upper = int(min(255.0, (1.0 + sigma) * median))

            # Canny Edge Detection
            query_edges[query_frame_idx] = cv2.Canny(
                blur,
                lower,
                upper,
            )

            if visualize:
                cv2.imwrite(f'{query_path}/{query_frame_idx}.jpg', query_edges[query_frame_idx])

    return query_edges


def online_processing(query_path):
    edges, video_to_index = load_canny_edges()
    query_edges = load_query_edges(query_path, visualize=False)

    # Sliding window configuration below
    sw_size, sw_jump = 150, 15
    sw_ranker = {}

    for k, v in video_to_index.items():
        if k not in sw_ranker:
            sw_ranker[k] = []
        for i in range(0, edges[v].shape[0] - sw_size + 1, sw_jump):
            sw_ranker[k].append(np.linalg.norm(edges[v][i:i + sw_size] - query_edges))
    return sw_ranker


def main():
    # videos, video_to_index = fast_load_db(VIDEO_DB)
    # offline_processing_canny_edge_detection(videos, video_to_index)
    # online_processing(sys.argv[1])
    pass


if __name__ == '__main__':
    main()
