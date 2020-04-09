"""
Transform video to images


Example usage:
python video2frame.py --pathIn examples/testvideo.mp4 --pathOut images/test
"""

import argparse
import os

import cv2

print(cv2.__version__)


def extractImages(pathIn, pathOut, sampling=1000):
    print('Extract video from %s every %d ms'%(pathIn, sampling))
    if not os.path.exists(pathOut):
        os.makedirs(pathOut)
    count = 0
    try:
        vidcap = cv2.VideoCapture(pathIn)
        success, image = vidcap.read()
    except Exception:
        print('Input video not found')
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * sampling))  # added this line
        success, image = vidcap.read()
        # print('Read a new frame: ', success)
        try:
            cv2.imwrite(pathOut + "/frame%05d.jpg" % count, image)  # save frame as JPEG file
        except Exception as e:
            print('Exception:', e)
        count = count + 1
    return count


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--pathIn", help="path to video")
    a.add_argument("--pathOut", help="path to images")
    a.add_argument("--sampling", help="samping frequency in ms", default=1000, type=int)
    args = a.parse_args()
    print(args)
    number_image = extractImages(args.pathIn, args.pathOut, args.sampling)
    print('%d images extracted to %s'%(number_image,args.pathOut))
