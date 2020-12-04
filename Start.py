# Start.py
import cv2
import Core
import VideoToFrames
import FramesToVideo


def start(frame, index, fps):
    logi = open('logizzz.txt', 'a')
    imgOriginalScene = frame
    x, tablica = Core.core(imgOriginalScene)
    timestamp = (index + 1) / fps
    logi.write(str(timestamp) + "; " + tablica + "\n")
    logi.close()
    return x


if __name__ == "__main__":
    VideoToFrames.read("Videos/grupaA3.mp4", "proj.avi")