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


def core(imgOriginalScene):
    # TODO usunąć poniższą linię
    # a = time.time()
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()  # Próba treningu KNN

    if not blnKNNTrainingSuccessful:  # if KNN training was not successful
        return imgOriginalScene, "Błędny trening KNN"

    # Wykrywanie Tablic i znaków na nich
    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)
    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)

    # TODO usunąć poniższą linię
    # cv2.imshow("imgOriginalScene", imgOriginalScene)

    if len(listOfPossiblePlates) == 0:
        return imgOriginalScene, "Nie wykryto tablicy"
    else:
        # Regex na sprawdzenie wykrytych tablic
        # FIXME
        pattern = re.compile(r"^[BCDEFGKXLNO0PRSTWZ2][A-Z02][A-Z0-9]+$")
        copyListOfPossiblePlates = listOfPossiblePlates
        for plate in listOfPossiblePlates:
            temp = cv2.boxPoints(plate.rrLocationOfPlateInScene)
            a = dist(temp[1], temp[2])/dist(temp[0], temp[1])
            b = dist(temp[0], temp[1])/dist(temp[1], temp[2])
            if 4.7 > max(a, b) > 4.4:
                if bool(pattern.match(plate.strChars)) and 10 > len(plate.strChars) > 6:
                    plate.regex = True
                else:
                    plate.regex = False
                if bool(re.search(r"(\w)\1\1", plate.strChars)):
                    plate.regex = False
            else:
                plate.regex = False
                # print("tablica " + plate.strChars + " regex: " + str(plate.regex))
        # print("----------------------------------------------")
        # listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)
        licPlate = []

        for plate in listOfPossiblePlates:
            if plate.regex:
                licPlate.append(plate)
        # licPlate = listOfPossiblePlates[0]
        if licPlate is None:
            return imgOriginalScene, "Nie wykryto tablicy"

        # TODO usunąć 2 poniższe linie
        # cv2.imshow("imgPlate", licPlate.imgPlate)
        # cv2.imshow("imgThresh", licPlate.imgThresh)
        """
        if len(licPlate.strChars) == 0:
            # print("\nno characters were detected\n\n")
            return imgOriginalScene, "Błąd rozpoznawania znaków na tablicy"
        """
        strNumbers = ""
        for plate in licPlate:
            # print(plate.strChars)
            drawRedRectangleAroundPlate(imgOriginalScene, plate)
            strNumbers = strNumbers + plate.strChars + ";"
        # print("---------------------------------------")
        # TODO usunąć 5 lini
        # print("\nlicense plate read from image = " + licPlate.strChars + "\n")  # write license plate text to std out
        # print("----------------------------------------")
        # cv2.imshow("imgOriginalScene", imgOriginalScene)  # re-show scene image
    # b = time.time() - a
    # print(b)

    return imgOriginalScene, strNumbers


def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):
    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)
