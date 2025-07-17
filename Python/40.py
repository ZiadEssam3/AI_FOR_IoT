import cv2
print(cv2.__version__) 

class mpFaceMesh:
    import mediapipe as mp 
    def __init__(self,still=False,numFaces = 3,tol1=.5,tol2=.5,drawMesh = True):
        # set our mediapipe object 
        self.myFaceMesh = self.mp.solutions.face_mesh.FaceMesh(
            static_image_mode=still,          
            max_num_faces=numFaces,                  
            min_detection_confidence=tol1,     
            min_tracking_confidence=tol2      
        )
        # draw mesh 
        self.myDraw = self.mp.solutions.drawing_utils
        self.draw = drawMesh  
    # analyze a frame 
    def Marks(self,frame):
        global width 
        global height
        # frame from open cv to mediapipe from BGR TO RGB
        # you got the frame  
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        # we are ready to analyze it 
        results = self.myFaceMesh.process(frameRGB)
        # now we get the data ... then we need to process the data 
        facesMeshLandMarks = [] # will have all faces array of arrays 
        if results.multi_face_landmarks != None: # means if we have data we will step throw the faces 
            # step thow the faces one face at a time 
            for faceMesh in results.multi_face_landmarks:
                faceMeshLandMarks = [] # set of landmarks assosiated with one face at a time 
                for lm in faceMesh.landmark:
                    loc = (int(lm.x*width),int(lm.y*height))
                    faceMeshLandMarks.append(loc)
                facesMeshLandMarks.append(faceMeshLandMarks)
                # do the automated mapping of the landmark of the face 
                if self.draw == True:
                    self.myDraw.draw_landmarks(frame,faceMesh)
        return facesMeshLandMarks
        
class mpFace:
    import mediapipe as mp 
    def __init__(self):
        # create the object 
        self.myFace = self.mp.solutions.face_detection.FaceDetection()
    # method that actually : find the face (do the analysis) 
    def Marks(self,frame):
        # we have the fram in the right color space  and can do the analysis
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        # return the analysis in variable results 
        results = self.myFace.process(frameRGB)
        faceBoundBoxs = []
        if results.detections != None: # it found something 
            # step throw the thing found 
            for face in results.detections:
                bBox = face.location_data.relative_bounding_box
                # draw a box around someone face i need 
                # 1- topleft , 2- bottom right 
                topLeft = (int(bBox.xmin*width),int(bBox.ymin*height))
                bottomRight = (int((bBox.xmin+bBox.width)*width),int((bBox.ymin+bBox.height)*height))
                faceBoundBoxs.append((topLeft,bottomRight))
        return faceBoundBoxs
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
        handsType = []
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            
            for hand in results.multi_handedness:
                handType = hand.classification[0].label
                handsType.append(handType)
            
            for handLandMarks in results.multi_hand_landmarks:
                myHand = []
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands,handsType
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
# create objects 
findHands = mpHands(2)
findPose  = mpPose(False,False,False)
findFace  = mpFace()
findMesh  = mpFaceMesh(drawMesh=False)

font = cv2.FONT_HERSHEY_SIMPLEX
fontColor = (0,0,255)
fontSize  = .4
fontThick = 1

""" Track bar """
def setLower (value):
    global lowerLimit
    lowerLimit = value 
def setUpper (value):
    global upperLimit
    upperLimit = value

lowerLimit = 0 
upperLimit = 468
cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars',width+50,0)
cv2.resizeWindow('Trackbars',400,150)

cv2.createTrackbar('lowerLimit','Trackbars',0,468,setLower)
cv2.createTrackbar('upperLimit','Trackbars',468,468,setUpper)

while True:
    ignore,frame = cam.read()  
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    flipped_frame = cv2.resize(flipped_frame,(width,height))
    """************* Do The Magic *******************"""
    # find some thing 
    handsLM,handsType = findHands.Marks(flipped_frame)
    faceLoc = findFace.Marks(flipped_frame)
    posLM = findPose.Marks(flipped_frame)
    facesMeshLM = findMesh.Marks(flipped_frame)
    """ ******** do some thing *********"""
    # for Hand
    for hand,handType in zip(handsLM,handsType):
        if handType == 'Right':
            lbl = 'Right'
        if handType == 'Left':
            lbl = 'Left'
        cv2.putText(flipped_frame,lbl,hand[8],font,2,fontColor,2) 
    # for Face 
    for face in faceLoc:
        cv2.rectangle(flipped_frame,face[0],face[1],(255,0,0),3)
    # for whole body
    if posLM != []:
        for ind in [13,14,15,16]:
            cv2.circle(flipped_frame,posLM[ind],20,(0,255,0),-1)
    # for faceMesh 
    for faceMeshLM in facesMeshLM:
        # got and put number at the face locations 
        cnt = 0
        for lm in faceMeshLM:
            if cnt >= lowerLimit and cnt <= upperLimit:
                cv2.putText(flipped_frame,str(cnt),lm,font,fontSize,fontColor,fontThick)
            cnt = cnt + 1 

    #show the frame 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()