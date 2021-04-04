print("Initializing the Program.............")
print()
print("Select an Image of Sudoku Board .............")

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import cv2
import numpy as np
from sudoku_solver_project.helpMe import *
from sudoku_solver_project.sudoku_solver import solve


def callMe(path):
    # set the width and height
    pathImage = path
    heightImg = 450
    widthImg = 450
    model = initializePredictionModel()

    # prepare the image
    img = cv2.imread(pathImage)
    img = cv2.resize(img, (widthImg, heightImg))
    imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)
    imgThreshold = preProcessing(img)

    # find all the contours
    imgContour = img.copy()
    imgBigContour = img.copy()
    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContour, contours, -1, (0, 255, 0), 3)

    # find the biggest contours
    biggest, maxArea = biggestContour(contours)
    # print(biggest)

    if len(biggest) != 0:
        biggest = reorder(biggest)
        # print(biggest)

        # draw 4 dots over "imgBigContour" image to understand
        cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 25)

        # [[a, b], [c, d], [e, f], [g, h]]
        pts1 = np.float32(biggest)
        # [[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]]
        pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])

        # convert it to a standard image specification from[[a, b], [c, d], [e, f], [g, h]] to  [0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        # print(matrix)
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
        imgWarpColored = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)

        imgDetectedDigits = imgBlank.copy()

        # split the warpedImage into 9X9 = 81 images
        # call splitBoxes() function the warped image into boxes to predict the numbers from our trained model
        boxes = splitBoxes(imgWarpColored)
        # print(len(boxes))

        print("Predicting the numbers from the images ....")
        # predict the numbers from the images that we store in boxes[] list after splitting the warped image
        numbers = getPredection(boxes, model)
        # print(numbers)
        print("Prediction complete .......")

        # displaying predicted numbers on a blank image
        imgDetectedDigits = displayNumbers(imgDetectedDigits, numbers, (255, 0, 255))

        # convert the number list to an numpy array to perform some numpy function on that array
        numbers = np.asarray(numbers)

        # add the placeholder where the sudoku board is blank i.e. we have to solve
        # i.e. we place a 1 where there is a blank and a 0 where there is a number to get a better understand
        posArray = np.where(numbers > 0, 0, 1)
        # print(posArray)

        ###########################################
        # find the solution of the board
        ###########################################

        # split the numbers array into 9 rows
        board = np.array_split(numbers, 9)
        # print(board)
        try:
            # call the solve() function from sudoku solver
            print("Solving the given sudoku board ....")
            solve(board)
            print("Solution Ready ....")
        except:
            pass
        # print(board)

        # we convert the 9 X 9 to 1D array to pass it in displayNumbers() function
        flatList = []
        for subList in board:
            for item in subList:
                flatList.append(item)

        # now just multiply this flatten[] list with posArray[] to only focus on the solved or predicted numbers
        solvedNumbers = flatList * posArray

        imgSolvedDigit = imgBlank.copy()
        imgSolvedDigit = displayNumbers(imgSolvedDigit, solvedNumbers)

        # now we have to put the solution to the original image
        # i.e. we have to unWarped the warped image
        # i.e. we just alternate the pts1 and pts2
        pts2 = np.float32(biggest)
        # [[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]]
        pts1 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        # print(matrix)
        imgInvWarpColored = img.copy()
        imgInvWarpColored = cv2.warpPerspective(imgSolvedDigit, matrix, (widthImg, heightImg))
        inv_perspective = cv2.addWeighted(imgInvWarpColored, 1, img, 0.5, 1)
        imgDetectedDigits = drawGrid(imgDetectedDigits)
        imgSolvedDigits = drawGrid(imgSolvedDigit)
        imgSolvedDigits = drawGrid(imgInvWarpColored)

    print("Showing the Solution on the given Sudoku board ......")
    print("Press 'q' to close the Solution window ......")
    cv2.putText(imgBlank, "<-- UNSOLVED", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    cv2.putText(imgBlank, "SOLVED -->", (230, heightImg - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    while True:
        imageArray = [[img, imgBlank, inv_perspective]]
        stackedImage = stackImages(imageArray, 0.6)

        cv2.imshow("Solution Window", stackedImage)
        key = cv2.waitKey(27)
        if key == ord('q'):
            print("Solution window closed .......")
            print()
            print("----------------------------------------------------------------------------------")
            print("Select an Sudoku Board image again .......")
            print()
            break
    cv2.destroyAllWindows()

