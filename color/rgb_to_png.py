from PIL import Image
import os
import glob
import numpy as np

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

def convert(rgb_dir, dest_dir):
    counter = 1
    query_frames = read_video(rgb_dir)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for frame in query_frames:
        png_img = Image.fromarray(frame, 'RGB')
        str_counter = str(counter)
        if counter < 10:
            str_counter = "00" + str(counter)
        elif counter < 100:
            str_counter = "0" + str(counter)
        png_img.save('{}/frame{}.png'.format(dest_dir, str_counter))
        counter += 1

if __name__ == "__main__":
    print("Hello World!")
    # convert()