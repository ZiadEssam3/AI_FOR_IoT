import cv2
print(cv2.__version__)   
import numpy as np
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
findHands = mpHands(1)
# array of the key landmarks 0,4,5,9,13,17,8,12,16,20
keyPoints = [0,4,5,9,13,17,8,12,16,20]
train = True
# take the hand and find all the distances between all the points for the keypoints 
# so it will be multi row distance array 
def findDistances(handData):
    distMatrix = np.zeros([len(handData),len(handData)],dtype='float')
    for row in range(0,len(handData)):
        for column in range(0,len(handData)):
            # calculate the distances 
            distMatrix[row][column] = ((handData[row][0]-handData[column][0])**2)+((handData[row][1]-handData[column][1])**2)**(1./2.)
    return distMatrix        

def findError(gestureMatrix,unKnownMatrix,keyPoints):
    error = 0 
    for row in keyPoints:
        for column in keyPoints:
            # compare the distance of known to the distance of unknown 
            error = error + abs(gestureMatrix[row][column]-unKnownMatrix[row][column])
    return error

while True:
    ignore,frame = cam.read()  
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    flipped_frame = cv2.resize(flipped_frame,(width,height))
    handData = findHands.Marks(flipped_frame)
    if train == True:
        if handData != []:
            print('Show Your Gesture, Press T when Ready! ')
            if cv2.waitKey(1) & 0xff == ord('t'):
                knownGesture = findDistances(handData[0])
                train = False
                print(knownGesture)
    if train == False: 
        if handData != []:
            unkownGesture = findDistances(handData[0])
            error = findError(knownGesture,unkownGesture,keyPoints)
            cv2.putText(flipped_frame,str(int(error)),(100,175),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),8)
    for hand in handData:
        for index in keyPoints: # [0,5,6,7,8]
            cv2.circle(flipped_frame,hand[index],10,(0,0,255),2)
    


    #show the frame 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
