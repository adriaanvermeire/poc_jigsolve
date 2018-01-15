import cv2
import os, sys
import numpy as np

# TODO: get images from commandline
# TODO: use mask in matchTemplate for srcImg

if __name__ == '__main__':
    arg = sys.argv
    srcImg = arg[1]
    patternImg = arg[2]
    matchImg = 'match.jpeg'

    if(os.path.isfile(srcImg) and os.path.isfile(patternImg)):
        source = cv2.imread(srcImg)
        pattern = cv2.imread(patternImg)
        match = cv2.imread(srcImg)
    else:
        raise ValueError

    imgray = cv2.cvtColor(pattern, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros(pattern.shape, np.uint8)
    cv2.drawContours(mask, contours, -1, (255), 5)

    # img.shape returns tuple (height, width, # color channels (usually 3))
    # [:2] limits the tuple returned to the first 2 (ignoring the color channels)
    patternHeight, patternWidth = pattern.shape[:2]

    result = cv2.matchTemplate(source, pattern, cv2.TM_SQDIFF)
    # After the function finishes the comparison,
    # the best matches can be found as global minimums (when CV_TM_SQDIFF was used)
    # or maximums (when CV_TM_CCORR or CV_TM_CCOEFF was used)
    # using the minMaxLoc() function
    minLoc, maxLoc = cv2.minMaxLoc(result)[2:]

    # to draw a rectangle at matching spot we need the upperleft corner (the returned point from minMaxLoc)
    # and lowerright corner (calculated with pattern's width and height)
    upperLeft = minLoc
    lowerRight = (minLoc[0] + patternWidth, minLoc[1] + patternHeight)
    cv2.rectangle(match, upperLeft, lowerRight, (255, 0, 0), 3)

    cv2.imwrite(matchImg, match)
    cv2.namedWindow('Matched Image', cv2.WINDOW_NORMAL)
    cv2.imshow('Matched Image', match)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
