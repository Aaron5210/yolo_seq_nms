# yolo_seq_nms
add seq_nms on yolo v2 for video object detection

This project combines **YOLOv2**([reference](https://arxiv.org/abs/1506.02640)) and **seq-nms**([reference](https://arxiv.org/abs/1602.08465)) to realise **real time video detection**.

## Steps

- Install `Tensorflow Object Detction API`([reference](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md));
- Modify the `Makefile` file according to your environment.
```
GPU=1		# 0 if your pc doesn't support CUDA
CUDNN=1		# 0 if your pc doesn't support CUDNN
OPENCV=1	# 0 if your pc doesn't support OPENCV
```
- `make` the project;
- Download `yolo.weights` and `tiny-yolo.weights` by running:
```bash
wget https://pjreddie.com/media/files/yolo.weights
wget https://pjreddie.com/media/files/tiny-yolo-voc.weights
```
- Copy a video file to the video directory, for example, `input.mp4`;
- From the video directory, run:
```bash
python video2img.py input.mp4
```
- Return to root directory and run: 
```
python yolo_seqnms.py
```
- **Attention: This scipt will fail if Tensorflow Object Detection API is not installed**;
- If you want a fatser detect, run:
```
python yolo_seqnms.py tiny
```
- If you only want to detect person, run:
```
python yolo_seqnms.py only_person
```
- If you want to reconstruct a video from these output images, you can go to the video directory and run:
```
python img2video.py output.mp4
```
- If you want to watch the video after creat it, run:
```
python img2video.py output.mp4 play
```

## Results

Here’s what I got from running my model over a demo video. Clic the image to watch the video on Youtube.

[![Watch the video](img/index.jpg)](https://www.youtube.com/watch?v=XC-3qXT0NsY)

## Reference

This project copies lots of code from [darknet](https://github.com/pjreddie/darknet) , [Seq-NMS](https://github.com/lrghust/Seq-NMS) and  [models](https://github.com/tensorflow/models).
