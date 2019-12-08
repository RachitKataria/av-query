from color_histogram import read_video
import numpy as np
import json
import sys
import cv2
import heapq

HISTOGRAM_JSON = "../data/histograms/videos.json"
HISTOGRAMS = "../data/histograms/videos.npy"
SL_SIZE = 15
NUM_VIDEOS = 7

def compare_frames(query_frames, video_frames):

    diff_list = np.subtract(query_frames, video_frames)
    diff = np.linalg.norm(diff_list, axis=3)

    return np.sum(diff)

def get_matches(query_dir):

    # Get histograms from np.save
    hists = np.load(HISTOGRAMS)

    # Load json that maps video type to number
    file = open(HISTOGRAM_JSON)
    hist_map = json.load(file)
    names = ["" for _ in range(NUM_VIDEOS)]

    for name, idx in hist_map.items():
        names[idx] = name

    # Get color histogram for each query frame
    query_frames = read_video(query_dir)
    query_frames = np.flip(query_frames, 3)
    query_frames = np.asarray(query_frames)

    # Get color histogram for query
    video = []
    for frame in query_frames:
        frame_feature = []
        img_yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        # sanity_check(frame, img_yuv)
        chans = cv2.split(img_yuv)
        colors = ("b", "g", "r")

        for (chan, color) in zip(chans, colors):
            hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
            frame_feature.append(hist)

        video.append(frame_feature)

    # Heap to store top k differences
    heap = []

    # Get best videos
    for num, video_frames in enumerate(hists):

        best_diff = sys.maxsize

        for beg_idx in range(0, 450, SL_SIZE):
            diff = compare_frames(video, video_frames[beg_idx:beg_idx+150])
            if diff < best_diff:
                best_diff = diff

        print("Compared query with {}! Got a difference of {}".format(names[num], best_diff))
        if len(heap) == 3:
            if heap[0][1]*-1 > best_diff:
                heapq.heappushpop(heap, (num, -1*best_diff))
        else:
            heapq.heappush(heap, (num, -1*best_diff))
    
    heap = sorted(heap, key=lambda x: -1*x[1])
    return (names[heap[0][0]], names[heap[1][0]], names[heap[2][0]])

if __name__ == "__main__":
    query_dir = sys.argv[1]
    top_3_matches = get_matches(query_dir)
    print(top_3_matches)


