from PIL import Image
import os

VIDEO_DB_PATH = '../data/query/third'
VIDEO_PATH_RGB = '../data/query/third_rgb'

def convert():
    counter = 1
    pngs = os.listdir(VIDEO_DB_PATH)
    pngs.sort()
    for png_path in pngs:
        img = Image.open("{}/{}".format(VIDEO_DB_PATH, png_path))
        rgb_img = img.convert('RGB')
        str_counter = str(counter)
        if counter < 10:
            str_counter = "00" + str(counter)
        elif counter < 100:
            str_counter = "0" + str(counter)
        rgb_img.save('{}/frame{}.rgb'.format(VIDEO_PATH_RGB, str_counter))
        counter += 1

if __name__ == "__main__":
    convert()