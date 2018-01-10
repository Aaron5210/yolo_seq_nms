# -*- coding: utf-8 -*-
import numpy as np
import cv2
import time
import copy
#import cPickle as pickle
import os, sys
from matplotlib import pyplot as plt
from PIL import Image
import scipy.misc
import yolo_detection
import visualization_utils as vis_util
import label_map_util
from seq_nms import *

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

def get_labeled_image(image_path, path_to_labels, num_classes, boxes, classes, scores):
    label_map = label_map_util.load_labelmap(path_to_labels)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=num_classes,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    image = Image.open(image_path)
    image_np = load_image_into_numpy_array(image)
    image_process = vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        boxes,
        classes,
        scores,
        category_index)
    return image_process

if __name__ == "__main__":
    # load image
    load_begin=time.time()
    pkllistfile=open(os.path.join('video', 'pkllist.txt'))
    pkllist=pkllistfile.readlines()
    pkllistfile.close()
    pkllist=[pkl.strip() for pkl in pkllist]
    load_end=time.time()
    print('load: {:.4f}s'.format(load_end - load_begin))

    # detection
    detect_begin=time.time()
    if len(sys.argv) > 1 and sys.argv[1]=='tiny':
        res = yolo_detection.detect_imgs(pkllist, cfg="cfg/tiny-yolo.cfg", weights="tiny-yolo.weights", nms=0, thresh=0.25)
    else:
        res = yolo_detection.detect_imgs(pkllist, nms=0, thresh=0.25)
    detect_end=time.time()
    print('total detect: {:.4f}s'.format(detect_end - detect_begin))
    print('average detect: {:.4f}s'.format((detect_end - detect_begin)/len(pkllist)))

    # nms
    nms_begin=time.time()
    if len(sys.argv) > 1 and sys.argv[1]=='only_person':
        boxes, classes, scores = dsnms(res, only_person=True)
    else:
        boxes, classes, scores = dsnms(res)
    nms_end=time.time()
    print('total nms: {:.4f}s'.format(nms_end - nms_begin))

    # save&visualization
    save_begin=time.time()
    PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
    NUM_CLASSES = 80
    if not os.path.exists('video/output'):
        os.makedirs('video/output')
    for i, image_path in enumerate(pkllist):
        image_process = get_labeled_image(image_path, PATH_TO_LABELS, NUM_CLASSES, np.array(boxes[i]), np.array(classes[i]), np.array(scores[i]))
        #plt.imshow(image_process)
        #plt.show()
        scipy.misc.imsave('video/output/frame{}.jpg'.format(i), image_process)
        if i%100==0:
            print('finish writing image{}'.format(i))
    save_end=time.time()
    print('total writing images: {:.4f}s'.format(save_end - save_begin))
