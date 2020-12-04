import cv2
import numpy as np
import time


def read(pathOfVideo, pathOfFrames):
    cap = cv2.VideoCapture(pathOfVideo)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # length of movie in frames
    frames = []
    for i in range(length):
        _, frame = cap.read()
        if frame is None:
            break
        frame = frame[55:-55]
        frames.append(frame)
    #  cv2.imwrite(pathOfFrames+"frame"+str(i)+".jpg", frame)

    return frames


if __name__ == "__main__":
    import cv2

    img = cv2.imread("frames/frame0.jpg")
    crop_img = img[55:-55]
    cv2.imshow("cropped", crop_img)
    cv2.waitKey(0)
    cv2.imshow("cropped", img)
    cv2.waitKey(0)
