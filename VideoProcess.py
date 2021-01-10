# VideoProcess.py

import cv2
import Start
import magic


def read(pathOfVideo, pathOfNewVideo):
    dirPath = pathOfNewVideo
    pathOfNewVideo = pathOfNewVideo + "/zmodyfikowane.avi"

    mime = magic.Magic(mime=True)
    filename = mime.from_file(pathOfVideo)
    if filename.find('video') == -1:
        return 1

    cap = cv2.VideoCapture(pathOfVideo)
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # length of movie in frames
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # przetwarzanie klatek
    for i in range(frameCount):
        _, frame = cap.read()

        # pobranie parametrów klatki z filmu
        if i == 0:
            height, width, layers = frame.shape
            size = (width, height)
            out = cv2.VideoWriter(pathOfNewVideo, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

        if frame is None:
            break
        # wykrywanie tablic
        newFrame = Start.start(frame, i, fps, dirPath)

        # dopisanie przetworzonej klatki do nowego filmu
        out.write(newFrame)

    out.release()
    cap.release()

    return 0
