# Start.py

import Core


def start(frame, index, fps, dirPath):
    logi = open(dirPath + "/logi.txt", 'a')
    imgOriginalScene = frame
    x, tablica = Core.core(imgOriginalScene)
    timestamp = (index + 1) / fps
    logi.write(str(timestamp) + "; " + tablica + "\n")
    logi.close()
    return x
