# Main.py

import cv2
import numpy as np
import os
import sys
import time
import DetectChars
import DetectPlates
import PossiblePlate

SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

# def video_feed(video_input):
#     print(video_input)
#     cap = cv2.VideoCapture(0)
#     # cap = video_input
#     # Trained XML classifiers describes some features of some object we want to detect
#     car_cascade = cv2.CascadeClassifier('D:\Code\Python\practice_everyting\ML\licence-plate-recognition-python-opencv-master\cars.xml')
#     # loop runs if capturing has been initialized.
    
#     while True:
#         # reads frames from a video
#         ret, frames = cap.read()
#         # re = np.array(cv2.resize(cap,(600,450),fx=0,fy=0, interpolation = cv2.INTER_CUBIC))
#         # convert to gray scale of each frames
#         gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
#         # Detects cars of different sizes in the input image
#         cars = car_cascade.detectMultiScale(frames, 1.1, 1)
#         # To draw a rectangle in each cars
#         for (x,y,w,h) in cars:
#             cv2.rectangle(frames,(x,y),(x+w,y+h),(0,0,255),2)
#             cv2.imshow('video2',frames)
#             car = frames[y:y+h, x:x+h]
#             FileName = "cars_" + str(y) + ".jpg"
#             cars = cv2.imwrite(FileName,car)
#             # Wait for Esc key to stop
#         if cv2.waitKey(33) == 27:
#         #     sys.exit()
#     # De-allocate any associated memory usage
#             cv2.destroyAllWindows()
#             print(car)
#             return(FileName)

def main():

    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()         # attempt KNN training

    if blnKNNTrainingSuccessful == False:                   # if KNN training was not successful
        print("\nerror: KNN traning was not successful\n")  # show error message
        return                                              # and exit program
    # end if

    video_input = 'http://192.168.1.109/mjpeg/1'
    # video_input = 0
    
    # imgOriginalScene  = cv2.imread(video_feed(video_input))  # open image
    imgOriginalScene = cv2.VideoCapture(video_input)
    licPlate_char =[]
   
    while True:
        pic = 0
        # reads frames from a video
        ret, frames = imgOriginalScene.read()
        # re = np.array(cv2.resize(cap,(600,450),fx=0,fy=0, interpolation = cv2.INTER_CUBIC))
        # convert to gray scale of each frames
        gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("gray", gray)            # show scene image
        # if imgOriginalScene is None:                            # if image was not read successfully
        #     print("\nerror: image not read from file \n\n")     # print error message to std out
        #     os.system("pause")                                  # pause so user can see error message
        #     return                                              # and exit program
        # # end if

        listOfPossiblePlates = DetectPlates.detectPlatesInScene(frames)           # detect plates

        listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates
        
        
        if len(licPlate_char) > 2:
            del licPlate_char[0]

        if len(listOfPossiblePlates) == 0:                          # if no plates were found
            # print("\nno license plates were detected\n")            # inform user no plates were found
            # cv2.imshow("gray", gray) 
            pass
        else:                                                       # else

            listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

            # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
            licPlate = listOfPossiblePlates[0]

            # cv2.imshow("imgPlate", licPlate.imgPlate)           # show crop of plate and threshold of plate
            cv2.imshow("imgThresh", licPlate.imgThresh)

            # if len(licPlate.strChars) == 0:                     # if no chars were found in the plate
            #     print("\nno characters were detected\n\n")  # show message
            #     return                                          # and exit program
            # # end if

            drawRedRectangleAroundPlate(frames, licPlate)             # draw red rectangle around plate
            # print("\nlicense plate read from image = " + licPlate.strChars + "\n")  # write license plate text to std out
            # licPlate_char = []
            licPlate_char.append(licPlate.strChars)
            if len(licPlate_char) > 2:
                    if licPlate_char[0] == '' and licPlate_char[1] == '' and licPlate_char[2] == '':
                        licPlate_char[0] = 'emty 1'
                        licPlate_char[1] = 'emty 2'
                        licPlate_char[2] = 'emty 3'
                    elif licPlate_char[0] == licPlate_char[1] == licPlate_char[2]:
                        print("\nlicense plate read from image = " + licPlate.strChars + "\n")
                        print("----------------------------------------")
                        print(licPlate_char)
                        # break
                    # print(licPlate_char)
            writeLicensePlateCharsOnImage(frames, licPlate)           # write license plate text on the image
            cv2.imshow("imgOriginalScene", frames)                # re-show scene imageqqq
            pic = pic+1
            cv2.imwrite("imgOriginalScene%s.png"%(pic), frames)           # write image out to file
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        # end if else

    # cv2.waitKey(0)					# hold windows open until user presses a key

    return

def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)            # get 4 vertices of rotated rect

    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 1)         # draw 4 red lines
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 1)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 1)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 1)

def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0                             # this will be the center of the area the text will be written to
    ptCenterOfTextAreaY = 0

    ptLowerLeftTextOriginX = 0                          # this will be the bottom left of the area that the text will be written to
    ptLowerLeftTextOriginY = 0

    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

    intFontFace = cv2.FONT_HERSHEY_SIMPLEX                      # choose a plain jane font
    fltFontScale = float(plateHeight) / 30.0                    # base font scale on height of plate area
    intFontThickness = int(round(fltFontScale * 1.5))           # base font thickness on font scale

    textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)        # call getTextSize

    ( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = licPlate.rrLocationOfPlateInScene

    intPlateCenterX = int(intPlateCenterX)              # make sure center is an integer
    intPlateCenterY = int(intPlateCenterY)

    ptCenterOfTextAreaX = int(intPlateCenterX)         # the horizontal location of the text area is the same as the plate

    if intPlateCenterY < (sceneHeight * 0.75):                                                  # if the license plate is in the upper 3/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))      # write the chars in below the plate
    else:                                                                                       # else if the license plate is in the lower 1/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))
    # end if

    textSizeWidth, textSizeHeight = textSize

    ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))           
    ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2)) 

            # write the text on the image
    cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, SCALAR_YELLOW, intFontThickness)

if __name__ == "__main__":
    main()


















