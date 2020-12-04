# Start.py
import cv2
import Core
import VideoToFrames
import FramesToVideo


def start(frame, index):
    logi = open('logiGRUPAA3.txt', 'a')
    # imgOriginalScene = cv2.imread("LicPlateImages/tes1.jpg")  # open image
    imgOriginalScene = frame
    x, tablica = Core.core(imgOriginalScene)  # Funkcja zwraza obraz z namalowanym prostokątem na tablicy
    # cv2.imshow("test", x)
    # timestamp [s] = (index+1)/25
    timestamp = (index + 1) / 25
    logi.write(str(timestamp) + "; " + tablica + "\n")
    # print("Start: ", tablica)
    logi.close()
    # cv2.waitKey(30)
    return x


if __name__ == "__main__":
    frames = VideoToFrames.read("Videos/grupaA3.mp4", "")
    print(len(frames))
    tablice = []
    counter = 0
    for frame in frames:
        tablice.append(start(frame, counter))
        counter += 1

    FramesToVideo.write(tablice)
