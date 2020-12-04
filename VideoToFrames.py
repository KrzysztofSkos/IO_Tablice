import cv2
import numpy as np
import time

import Start


def read(pathOfVideo, pathOfNewVideo):
    cap = cv2.VideoCapture(pathOfVideo)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # length of movie in frames
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    for i in range(length):
        _, frame = cap.read()
        if i == 0:
            height, width, layers = frame.shape
            size = (width, height)
            out = cv2.VideoWriter(pathOfNewVideo, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

        if frame is None:
            break
        newFrame = Start.start(frame, i, fps)
        out.write(newFrame)
    out.release()
    cap.release()
    return 0
