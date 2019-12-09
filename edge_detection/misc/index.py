import imageio
import json
import sys
import numpy as np


def main():
    # Load in cache/videos.npy
    videos = np.load('../cache/videos.npy')

    # Load in cache/video_to_index.json
    with open('../cache/video_to_index.json') as file:
        video_to_index = json.load(file)

    for k, v in video_to_index.items():
        imageio.mimwrite(f'../../data/database_videos/{k}/{k}.mp4', videos[v], fps=30)
        print(f'Wrote {k}.mp4 to ../../data/database_videos/{k}/{k}.mp4')


if __name__ == '__main__':
    main()