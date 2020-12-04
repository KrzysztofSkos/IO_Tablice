import cv2
import numpy as np
import glob


def write(frames):
    img_array = []
    for img in frames:
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter('projectGRUPAA3.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    return out


if __name__ == "__main__":

    tablice = []
    for i in range(38):
        tablice.append("LicPlateImages/frames/frame" + str(i) + ".jpg")

    write(tablice)
