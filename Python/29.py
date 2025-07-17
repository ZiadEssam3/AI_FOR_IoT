import cv2
print(cv2.__version__)
import mediapipe as mp
hands = mp.solutions.hands.Hands(static_image_mode=False,max_num_hands=2,min_detection_confidence=0.5,min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
""" Function For Creating Parsing and LandMarks"""
def parseLandmarks(frame):
    # array of arrays 
    myHands = []
    frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # analysis the frame 
    results = hands.process(frameRGB) # results is complicated data structue
    if results.multi_hand_landmarks != None:
        # results.multi_hand_landmarks ==> has all the data for all the hands 
        # handLandMarks0 ==> step throw 1 hand at a time 
        for handLandMarks in results.multi_hand_landmarks:
            # The land mark for 1 hand  
            myHand = []
            # step throw the individuals landmarks .. boom boom boom boom 
            for landmark in handLandMarks.landmark:
                myHand.append((int(landmark.x*width),int(landmark.y*height))) # and normalize to the actual pixel
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
while True:
    ignore,frame = cam.read()  
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    flipped_frame = cv2.resize(flipped_frame,(width,height))

    myHands = parseLandmarks(flipped_frame)
    for hand in myHands:
        for digit in [8,12,16,20]: # range(0,21,1)
            cv2.circle(flipped_frame,hand[digit],15,(255,255,0),-1)


    #show the frame 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
"""The data structure we want is look like """
# myHands = [[(x0,y0),(x1,y1),(x2,y2),...],[(x0,y0),(x1,y1),(x2,y2),...]]