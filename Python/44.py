import cv2
print(cv2.__version__)   
import numpy as np
import time
import pickle
class mpHands:
    import mediapipe as mp 
    def __init__(self,imgmode=False,maxHands=2,tol1=.5,tol2=.5):
        self.hands = self.mp.solutions.hands.Hands(static_image_mode=imgmode,max_num_hands=maxHands,min_detection_confidence=tol1,min_tracking_confidence=tol2)
    def Marks(self,frame):
        myHands = []
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for handLandMarks in results.multi_hand_landmarks:
                myHand = []
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands
""" Setting Up The Camera """
#setting the variables
width = 1280
height = 720
cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#set window width , height 
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
#set The Frame rate 30 frames per second
cam.set(cv2.CAP_PROP_FPS,30)
#set up the codec 
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
"""******************************************************"""
time.sleep(1)
findHands = mpHands(1)
# array of the key landmarks 0,4,5,9,13,17,8,12,16,20
keyPoints = [0,4,5,9,13,17,8,12,16,20]
train = int(input('Enter 1 to Train , 0 To Recognize'))
if train == 1:
    trainCnt = 0
    knownGestures = []
    numGest = int(input('How Many Gestures Do You Want? \n'))
    gestNames = []
    for i in range(0,numGest,1):
        prompt = 'Name of Gesture #' + str(i+1) + ' ' 
        name = input(prompt)
        gestNames.append(name)
    print(gestNames)
    trainName = input('Filename For Training Data? (Pree Enter for Default) \n')
    if trainName == '':
        trainName = 'default'
    trainName = './HRTrainData/' + trainName + '.pkl' # concatination with a string 

tol = 10
if train == 0: 
    # use the file 
    trainName = input('What Training Data Do You Want To Use? (Press Enter For Default) \n')
    if trainName == '':
        trainName = 'default'
    trainName = './HRTrainData/' + trainName + '.pkl'
    with open(trainName,'rb') as f:
        gestNames = pickle.load(f)
        knownGestures = pickle.load(f)


def findDistances(handData):
    distMatrix = np.zeros([len(handData),len(handData)],dtype='float')
    palmSize = np.sqrt((handData[0][0] - handData[9][0]) ** 2 + (handData[0][1] - handData[9][1]) ** 2)
    for row in range(0,len(handData)):
        for column in range(0,len(handData)):
            # calculate the distances 
            distMatrix[row][column] = (np.sqrt((handData[row][0] - handData[column][0]) ** 2 + (handData[row][1] - handData[column][1]) ** 2))/palmSize
    return distMatrix        
def findError(gestureMatrix,unKnownMatrix,keyPoints):
    error = 0 
    for row in keyPoints:
        for column in keyPoints:
            # compare the distance of known to the distance of unknown 
            error = error + abs(gestureMatrix[row][column]-unKnownMatrix[row][column])
    print(error)
    return error
# find gesture function 
def findGesture(unknownGesture,knownGestures,keypoints,gestNames,tol):
    errorArray = []
    for i in range(0,len(gestNames),1):
        error = findError(knownGestures[i],unknownGesture,keypoints)
        errorArray.append(error)
        errorMin = errorArray[0]
        minIndex = 0
    for i in range(0,len(errorArray),1):
        if errorArray[i] < errorMin:
            errorMin = errorArray[i]
            minIndex = i
    if errorMin < tol:
        gesture = gestNames[minIndex]
    if errorMin >= tol:
        gesture= 'UnKnown' 
    return gesture   
while True:
    ignore,frame = cam.read()  
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    flipped_frame = cv2.resize(flipped_frame,(width,height))
    handData = findHands.Marks(flipped_frame)
    """ Train Dataset """
    if train == 1:
        if handData != []:
            print('Please Show Gesture ',gestNames[trainCnt],': Press t when Ready')
            if cv2.waitKey(1) & 0xff == ord('t'):
                knownGesture = findDistances(handData[0])
                knownGestures.append(knownGesture)
                trainCnt = trainCnt+1
                if trainCnt == numGest:
                    train = 0
                    # save the training data 
                    with open(trainName,'wb') as f:
                        pickle.dump(gestNames,f)
                        pickle.dump(knownGestures,f)
    """ Recognize """
    if train == 0: 
        if handData != []:
            unkownGesture = findDistances(handData[0])
            myGesture = findGesture(unkownGesture,knownGestures,keyPoints,gestNames,tol)
            cv2.putText(flipped_frame,myGesture,(100,175),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),8)
    """ Do something After Recognation """
    for hand in handData:
        for index in keyPoints: # [0,5,6,7,8]
            cv2.circle(flipped_frame,hand[index],10,(0,0,255),2)
    #show the frame 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()