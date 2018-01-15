import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import sys
import argparse

# order_points and four_point_transform were copied and adjusted from this url:
# https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv.getPerspectiveTransform(rect, dst)
    warped = cv.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


def flattenPreview(preview):
    _gray = cv.cvtColor(preview, cv.COLOR_BGR2GRAY)
    _blurred = cv.GaussianBlur(_gray, (3, 3), 0)
    _canny = cv.Canny(_blurred, 50, 200)

    cnts = cv.findContours(_canny.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[1]
    cnts = sorted(cnts, key=cv.contourArea, reverse=True)[:5]

    for c in cnts:
        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    return four_point_transform(preview, screenCnt.reshape(4, 2))


def countPieces(pcs):
    count = 0
    for piece in pcs:
        length = cv.arcLength(piece, True)
        if length >= 300:
            count += 1
    return count

# Documentation on searchPiece can be found in searchPiece.py


def searchPiece(piece, pieceIndex, preview, match):
    grayPiece = cv.cvtColor(piece, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(grayPiece, 127, 255, 0)
    _, contours, _ = cv.findContours(
        thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    mask = np.zeros(piece.shape, np.uint8)
    cv.drawContours(mask, contours, -1, (255), 5)

    pieceHeight, pieceWidth = piece.shape[:2]

    result = cv.matchTemplate(preview, piece, cv.TM_SQDIFF)
    minLoc, maxLoc = cv.minMaxLoc(result)[2:]

    upperLeft = minLoc
    lowerRight = (minLoc[0] + pieceWidth, minLoc[1] + pieceHeight)
    cv.rectangle(match, upperLeft, lowerRight, (255, 0, 0), 3)
    cv.putText(match, str(pieceIndex),
               (upperLeft[0] + 30, upperLeft[1] + 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv.imwrite(args.match_path, match)


def siftThroughPreview(piece, preview, match):
    MIN_MATCH_COUNT = 4
    img1 = cv.cvtColor(piece, cv.COLOR_BGR2GRAY)          # queryImage
    img2 = cv.cvtColor(preview, cv.COLOR_BGR2GRAY)  # trainImage
    # Initiate SIFT detector
    sift = cv.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good) >= MIN_MATCH_COUNT:
        src_pts = np.float32(
            [kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32(
            [kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        M, mask = cv.findHomography(src_pts, dst_pts, 0, 5.0)
        matchesMask = mask.ravel().tolist()
        h, w = img1.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1],
                          [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv.perspectiveTransform(pts, M)
        match = cv.polylines(match, [np.int32(dst)], True, 255, 3, cv.LINE_AA)

    else:
        print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
        matchesMask = None

    draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                       singlePointColor=None,
                       matchesMask=matchesMask,  # draw only inliers
                       flags=2)
    match = cv.drawMatches(img1, kp1, match, kp2, good, None, **draw_params)


argparser = argparse.ArgumentParser(
    description='Match pieces in puzzlepreview.')
argparser.add_argument(
    'pieces_path', help='a path to the image with the to be matched puzzlepieces')
argparser.add_argument('-a', '--amountOfPieces', type=int,
                       help='the amount of pieces there are in the puzzlepieces image [-1 will automatically figure it out]', default='-1')
argparser.add_argument('-p', '--preview', dest='preview_path',
                       help='a path to the preview image of the puzzle')
argparser.add_argument('-m', '--match', dest='match_path',
                       help='name for image with matched puzzlepieces', default='match.jpg')

args = argparser.parse_args()

# Load image, convert to gray and blur it to minimize noise
img = cv.resize(cv.imread(args.pieces_path), (0, 0), None, .5, .5)
imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
_, gmask = cv.threshold(imgray, 127, 255, cv.THRESH_BINARY)
# cv.imshow('mask', gmask)
blurred = cv.GaussianBlur(imgray, (3, 3), 0)
# Apply canny filter to detect edges
edged = cv.Canny(blurred, 0, 40)

# Dilating is used to connect the individual contours that are close enough to eachother together
# This way one contours per piece is made
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
dilated = cv.dilate(edged, kernel)

# Find all elements that stand out in the picture (i.e. puzzle pieces)
_, cnts, _ = cv.findContours(
    dilated.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Filters out the right amount of puzzlepieces
if len(cnts) > 0:
    amountOfPieces = countPieces(
        cnts) if args.amountOfPieces < 0 else args.amountOfPieces
    pieces = sorted(cnts, key=cv.contourArea, reverse=True)[:amountOfPieces]

mask = np.zeros(img.shape, np.uint8)
cv.drawContours(mask, pieces, -1, (255, 255, 255), -1)

# Extract each piece and save to own file
for i, piece in enumerate(pieces):
    x, y, w, h = cv.boundingRect(piece)
    x2 = x + w
    y2 = y + h
    roi = img[y:y2, x:x2]
    pieceMask = mask[y:y2, x:x2]
    res = cv.bitwise_and(roi, pieceMask)
    # cv.imwrite('puzzlepiece' + str(i) + '.jpg', res)
    pieces[i] = res
    # cv.putText(img, str(i), (x + 30, y + 50),
    #            cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

preview = cv.imread(args.preview_path)
preview = flattenPreview(preview)
match = preview.copy()

# for index, piece in enumerate(pieces):
#     searchPiece(piece, index, preview, match)
# siftThroughPreview(piece, preview, match)

# Show the resulting images
cv.namedWindow('match', flags=cv.WINDOW_NORMAL + cv.WINDOW_KEEPRATIO)
cv.imshow('match', match)
# cv.imshow('canny', edged)
# cv.imshow('gray', imgray)
# cv.imshow('blurred', blurred)

cv.waitKey()
