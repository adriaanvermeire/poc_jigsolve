import cv2
import os

# TODO: get images from commandline
# TODO: use mask in matchTemplate for srcImg


if __name__ == '__main__':
    srcImg = 'image.JPG'
    patternImg = 'faulty.JPG'
    matchImg = 'match.jpeg'

    if(os.path.isfile(srcImg) and os.path.isfile(patternImg)):
        source = cv2.imread(srcImg)
        pattern = cv2.imread(patternImg)
        match = cv2.imread(srcImg)
    else:
        raise ValueError

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
    cv2.rectangle(match, upperLeft, lowerRight, (255,0,0), 1)

    cv2.imwrite(matchImg, match)
