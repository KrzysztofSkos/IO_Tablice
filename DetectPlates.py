# DetectPlates.py

import cv2
import math
from math import dist

import Preprocess
import DetectChars
import PossiblePlate
import PossibleChar

PLATE_WIDTH_PADDING_FACTOR = 1.3
PLATE_HEIGHT_PADDING_FACTOR = 1.5


def detectPlatesInScene(imgOriginalScene):
    listOfPossiblePlates = []

    cv2.destroyAllWindows()

    imgGrayscaleScene, imgThreshScene = Preprocess.preprocess(imgOriginalScene)

    # Znalezienie wszystkich możliwych znaków w klatce
    listOfPossibleCharsInScene = findPossibleCharsInScene(imgThreshScene)

    # Znalezienie grup znaków
    listOfListsOfMatchingCharsInScene = DetectChars.findListOfListsOfMatchingChars(listOfPossibleCharsInScene)

    # Próba znalezienia tablicy
    for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
        possiblePlate = extractPlate(imgOriginalScene, listOfMatchingChars)

        if possiblePlate.imgPlate is not None:
            temp = cv2.boxPoints(possiblePlate.rrLocationOfPlateInScene)
            a = dist(temp[1], temp[2]) / dist(temp[0], temp[1])
            b = dist(temp[0], temp[1]) / dist(temp[1], temp[2])
            if 4.7 > max(a, b) > 4.4:
                listOfPossiblePlates.append(possiblePlate)

    return listOfPossiblePlates


def findPossibleCharsInScene(imgThresh):
    listOfPossibleChars = []
    intCountOfPossibleChars = 0
    imgThreshCopy = imgThresh.copy()
    contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(0, len(contours)):
        possibleChar = PossibleChar.PossibleChar(contours[i])
        if DetectChars.checkIfPossibleChar(possibleChar):
            intCountOfPossibleChars = intCountOfPossibleChars + 1
            listOfPossibleChars.append(possibleChar)

    return listOfPossibleChars


def extractPlate(imgOriginal, listOfMatchingChars):
    possiblePlate = PossiblePlate.PossiblePlate()
    listOfMatchingChars.sort(key=lambda matchingChar: matchingChar.intCenterX)

    # Obliczenie centrum tablicy
    fltPlateCenterX = (listOfMatchingChars[0].intCenterX + listOfMatchingChars[
        len(listOfMatchingChars) - 1].intCenterX) / 2.0
    fltPlateCenterY = (listOfMatchingChars[0].intCenterY + listOfMatchingChars[
        len(listOfMatchingChars) - 1].intCenterY) / 2.0
    ptPlateCenter = fltPlateCenterX, fltPlateCenterY

    # Obliczenie jej wymiarów
    intPlateWidth = int((listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectX + listOfMatchingChars[
        len(listOfMatchingChars) - 1].intBoundingRectWidth - listOfMatchingChars[
                             0].intBoundingRectX) * PLATE_WIDTH_PADDING_FACTOR)
    intTotalOfCharHeights = 0
    for matchingChar in listOfMatchingChars:
        intTotalOfCharHeights = intTotalOfCharHeights + matchingChar.intBoundingRectHeight
    fltAverageCharHeight = intTotalOfCharHeights / len(listOfMatchingChars)
    intPlateHeight = int(fltAverageCharHeight * PLATE_HEIGHT_PADDING_FACTOR)

    # Obliczenie kąta korekcji
    fltOpposite = listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY - listOfMatchingChars[0].intCenterY
    fltHypotenuse = DetectChars.distanceBetweenChars(listOfMatchingChars[0],
                                                     listOfMatchingChars[len(listOfMatchingChars) - 1])
    fltCorrectionAngleInRad = math.asin(fltOpposite / fltHypotenuse)
    fltCorrectionAngleInDeg = fltCorrectionAngleInRad * (180.0 / math.pi)

    possiblePlate.rrLocationOfPlateInScene = (
        tuple(ptPlateCenter), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg)

    # Obracanie
    rotationMatrix = cv2.getRotationMatrix2D(tuple(ptPlateCenter), fltCorrectionAngleInDeg, 1.0)
    height, width, numChannels = imgOriginal.shape
    imgRotated = cv2.warpAffine(imgOriginal, rotationMatrix, (width, height))
    imgCropped = cv2.getRectSubPix(imgRotated, (intPlateWidth, intPlateHeight), tuple(ptPlateCenter))
    possiblePlate.imgPlate = imgCropped

    return possiblePlate
