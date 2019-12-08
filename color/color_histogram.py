import glob
import numpy as np
import os
import cv2
from PIL import Image
from matplotlib import pyplot as plt

VIDEO_DB_PATH = '../data/database_videos'

import cv2
import numpy as np


def make_lut_u():
    return np.array([[[i,255-i,0] for i in range(256)]],dtype=np.uint8)

def make_lut_v():
    return np.array([[[0,255-i,i] for i in range(256)]],dtype=np.uint8)

def read_video(path):
    rgbs = glob.glob(f'{path}/*.rgb')
    rgbs.sort()

    reds = []
    greens = []
    blues = []

    for f in rgbs:
        with open(f, 'rb') as file:

            # Don't use unless using .rgb files converted from png's gathered from youtube video using vlc
            # reds.append(np.flip(np.roll(np.asarray(Image.frombytes('L', (352, 288), file.read(352*288), 'raw')), -160), axis=0))
            # greens.append(np.flip(np.roll(np.asarray(Image.frombytes('L', (352, 288), file.read(352*288), 'raw')), -160), axis=0))
            # blues.append(np.flip(np.roll(np.asarray(Image.frombytes('L', (352, 288), file.read(352*288), 'raw')), -160), axis=0))

            reds.append(np.asarray(Image.frombytes('L', (352, 288), file.read(352*288), 'raw')))
            greens.append(np.asarray(Image.frombytes('L', (352, 288), file.read(352*288), 'raw')))
            blues.append(np.asarray(Image.frombytes('L', (352, 288), file.read(352*288), 'raw')))

    frames = np.stack((np.asarray(reds), np.asarray(greens), np.asarray(blues)), axis=-1)
    return frames

def sanity_check(img, img_yuv):
    y, u, v = cv2.split(img_yuv)
    lut_u, lut_v = make_lut_u(), make_lut_v()

    # Convert back to BGR so we can apply the LUT and stack the images
    y = cv2.cvtColor(y, cv2.COLOR_GRAY2BGR)
    u = cv2.cvtColor(u, cv2.COLOR_GRAY2BGR)
    v = cv2.cvtColor(v, cv2.COLOR_GRAY2BGR)

    u_mapped = cv2.LUT(u, lut_u)
    v_mapped = cv2.LUT(v, lut_v)

    result = np.vstack([img, y, u_mapped, v_mapped])
    cv2.imwrite('shed_combo.png', img)

def main():
    vids = []
    vid_names = []
    for video_path in os.listdir(VIDEO_DB_PATH):
        if video_path[0] != ".":
            print(f'Processing {VIDEO_DB_PATH}/{video_path}')
            vids.append(read_video(f'{VIDEO_DB_PATH}/{video_path}'))
            vid_names.append(video_path)

    vids = np.asarray(vids)

    # Get into BGR order
    vids = np.flip(vids, 4)
    features = []
    video_count = 0

    # sanity_check(vids[4][100], cv2.cvtColor(vids[4][100], cv2.COLOR_BGR2YUV))

    for vid in vids:
        frame_count = 0
        video = []
        for frame in vid:
            frame_feature = []
            img_yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
            # sanity_check(frame, img_yuv)
            chans = cv2.split(img_yuv)
            colors = ("b", "g", "r")

            for (chan, color) in zip(chans, colors):
                hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
                frame_feature.append(hist)

            frame_count += 1
            if frame_count % 100 == 0:
                print("Done with {} frames of {}".format(frame_count, vid_names[video_count]))
            video.append(frame_feature)

        features.append(video)
        video_count += 1

    np.save("videos", np.asarray(features))
                
if __name__ == '__main__':
    main()

    # Don't use unless using .rgb files converted from png's gathered from youtube video using vlc
    # query_frames = read_video("../data/query/third_rgb")
    # query_frames = np.asarray(query_frames)
    # query_frames = np.flip(query_frames, 3)
    # sanity_check(query_frames[100], cv2.cvtColor(query_frames[100], cv2.COLOR_BGR2YUV))


