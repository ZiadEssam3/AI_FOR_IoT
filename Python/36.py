import cv2
print(cv2.__version__)   

class mpPose:
    import mediapipe as mp 
    def __init__(self,still=False,upperbody=False,smoothData=True,tol1=.5,tol2=.5):
        print(still,upperbody,smoothData)
        self.myPose = self.mp.solutions.pose.Pose(
            static_image_mode = still,
            model_complexity  = upperbody,
            smooth_landmarks  = smoothData,
            min_detection_confidence = tol1,
            min_tracking_confidence  =  tol2
        ) 
    # the method done the work : find the landmarks 
    def Marks(self,frame):
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = self.myPose.process(frameRGB)
        poseLandmarks = []
        if results.pose_landmarks: 
            # step throw the landmarks 
            for lm in results.pose_landmarks.landmark:
                # set of tuple of (x,y) values 
                poseLandmarks.append((int(lm.x*width),int(lm.y*height)))
            # print(poseLandmarks)
        return poseLandmarks    
            
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

findHands = mpHands(False,2,.5,.5)
findPose  = mpPose(False,False,False)



while True:
    ignore,frame = cam.read()  
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    flipped_frame = cv2.resize(flipped_frame,(width,height))
    # find the Hand data 
    handData = findHands.Marks(flipped_frame)
    # do something with it 
    for hand in handData:
        for index in range(0,21,1): # [0,5,6,7,8]
            cv2.circle(flipped_frame,hand[index],10,(0,0,255),2)
    # find the pose data 
    poseData = findPose.Marks(flipped_frame)
    # do something with it 
    # if len(poseData) != 0:
            # cv2.circle(flipped_frame,poseData[0],5,(0,255,0),2)
    for pose in poseData:
        for index in range(0,33,1):
            cv2.circle(flipped_frame,poseData[index],5,(0,255,0),2)


    #show the frame 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
