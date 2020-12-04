# Core.py

import cv2
import numpy as np
import os
import time
import re
from math import dist

import DetectChars
import DetectPlates
import PossiblePlate

SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)


# Funkcja zwraza obraz z namalowanym prostokątem na tablicy oraz rozpoznane znaki
def core(imgOriginalScene):
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()  # Próba treningu KNN

    if not blnKNNTrainingSuccessful:
        return imgOriginalScene, "Błędny trening KNN"

    # Wykrywanie Tablic i znaków na nich
    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)
    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)

    if len(listOfPossiblePlates) == 0:
        return imgOriginalScene, "Nie wykryto tablicy"
    else:
        # Regex na sprawdzenie wykrytych tablic
        pattern = re.compile(r"^[BCDEFGKXLNO0PRSTWZ2][A-Z02][A-Z0-9]+$")
        for plate in listOfPossiblePlates:
            if bool(pattern.match(plate.strChars)) and 10 > len(plate.strChars) > 6:
                plate.regex = True
            else:
                plate.regex = False
            if bool(re.search(r"(\w)\1\1", plate.strChars)):
                plate.regex = False
        licPlate = []

        for plate in listOfPossiblePlates:
            if plate.regex:
                licPlate.append(plate)
        if licPlate is None:
            return imgOriginalScene, "Nie wykryto tablicy"

        strNumbers = ""
        for plate in licPlate:
            # print(plate.strChars)
            drawRedRectangleAroundPlate(imgOriginalScene, plate)
            strNumbers = strNumbers + plate.strChars + ";"

    return imgOriginalScene, strNumbers


def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):
    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)
