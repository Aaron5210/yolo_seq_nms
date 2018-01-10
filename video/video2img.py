from __future__ import print_function
import cv2
import os, sys
import glob
import time

def save_video_images_to_folder(file_name):
    # traet input folder
    if not os.path.exists('input'):
        os.makedirs('input')
    else:
        for root, dirs, files in os.walk('input'):
            for f in files:
                os.unlink(os.path.join(root, f))

    # read video
    vidcap = cv2.VideoCapture(file_name)
    string_to_write = ''
    count = 0
    start_time = time.time()
    while True:
      success,image = vidcap.read()
      if not success:
          break
      print('Read a new frame %-4d, time used: %8.2fs \r' % (count, time.time()-start_time), end="")
      cv2.imwrite(os.path.join('input', 'frame{}.jpg'.format(count)), image)     # save frame as JPEG file
      string_to_write += 'video/input/frame{}.jpg\n'.format(count)
      count += 1
    with open('pkllist.txt', 'w') as f:
        f.write(string_to_write)
        print("\npkllist.txt created.")

def main():
    file_name = sys.argv[1]
    save_video_images_to_folder(file_name)

if __name__ == "__main__":
   main()
