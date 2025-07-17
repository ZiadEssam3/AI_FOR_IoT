# According to the latest information, mediapipe officially supports Python versions 3.9 to 3.12
import cv2
print(cv2.__version__)
import mediapipe as mp 
# print(mp.__version__)
""" Setting up the camera """
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
""" Create object that does the hand detection """
hands = mp.solutions.hands.Hands(static_image_mode=False,max_num_hands=2,min_detection_confidence=0.5,min_tracking_confidence=0.5)
# draw the data (object)
mpDraw = mp.solutions.drawing_utils

while True:
    myHands = []
    ignore,frame = cam.read()  
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    flipped_frame = cv2.resize(flipped_frame,(width,height))
    frameRGB = cv2.cvtColor(flipped_frame,cv2.COLOR_BGR2RGB)
    # analyze that 
    results = hands.process(frameRGB)
    if results.multi_hand_landmarks != None:
        print(results)
        # start analyze step throw hands
        for handLandMarks in results.multi_hand_landmarks:
            myHand = []
            # Draw the hands 
            print(handLandMarks)
            # mpDraw.draw_landmarks(flipped_frame,handLandMarks,mp.solutions.hands.HAND_CONNECTIONS)
            # step throw the landmark of individual
            for Landmark in handLandMarks.landmark:
                print((Landmark.x,Landmark.y))
                myHand.append((int(Landmark.x*width),int(Landmark.y*height)))
            print('')
            # print(myHand)
            # detect the little pinky 
            cv2.circle(flipped_frame,myHand[17],25,(255,0,255),-1)
            cv2.circle(flipped_frame,myHand[18],25,(255,0,255),-1)
            cv2.circle(flipped_frame,myHand[19],25,(255,0,255),-1)
            cv2.circle(flipped_frame,myHand[20],25,(255,0,255),-1)
            myHands.append(myHand)
            print(myHands)
            print('')
    
    #show the frame 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',100,30)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
""" The datastructure we want looks like this """
# myHand  = [(x0,y0),(x1,y1),(x2,y2),....]
# myHands = [[myHand1],[myHand2]]