from __future__ import print_function
import cv2
import os, sys, getopt
import glob
import time

def generate_video(video_name):
    image_folder = 'output'
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    count = 0
    for element in os.listdir('output'):
        if(str(element).endswith('jpg')):
            count = count + 1
    images = ['frame{}.jpg'.format(i) for i in range(count)]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
    video = cv2.VideoWriter(video_name, fourcc, 30.0, (width,height))
    start_time = time.time()
    for count, image in enumerate(images):
        video.write(cv2.imread(os.path.join(image_folder, image)))
        print('(%d/%d)write a new frame, time used: %5.2fs \r' % (count, len(images), time.time()-start_time), end="")
    print('\n %s created.' % video_name)
    cv2.destroyAllWindows()
    video.release()

def play_video(video_name):
    cap = cv2.VideoCapture(video_name)
    paused = False
    delay = {True: 0, False: 1}
    while(True):
        ret, frame = cap.read()
        if not ret:
            cap = cv2.VideoCapture(video_name)
            ret, frame = cap.read()
        cv2.putText(frame, 'Press \'q\' to stop.', (20, 20), 0, 0.5, (0, 0, 255))
        cv2.putText(frame, 'Press \'p\' to pause.', (20, 40), 0, 0.5, (0, 0, 255))
        cv2.imshow('frame',frame)
        time.sleep(0.1)    #10fps
        key = cv2.waitKey(delay[paused])
        if key & 255 == ord('p'):
            paused = not paused

        if key & 255 == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def main():
    if len(sys.argv) > 1:
        video_name = sys.argv[1]
    else:
        print('usage: python img2video.py output.mp4')
        sys.exit(0)
    generate_video(video_name)
    if len(sys.argv) > 2 and sys.argv[2]=='play':
        play_video(video_name)


if __name__ == "__main__":
   main()
