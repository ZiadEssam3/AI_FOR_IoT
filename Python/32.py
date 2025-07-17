import cv2
print(cv2.__version__)   

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


# paddle variables 
paddleWidth  = 125
paddleHeight = 25 
paddleColor  = (0,0,255)
# ball variables 
ballRadius = 15
ballColor = (255,0,0)
# ball positions 
xPos = int(width/2)
yPos = int(height/2)
Deltax = 2
Deltay = 2
score = 0
lives = 5
font = cv2.FONT_HERSHEY_SIMPLEX
index = 8
while True:
    ignore,frame = cam.read()  
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    flipped_frame = cv2.resize(flipped_frame,(width,height))
    cv2.circle(flipped_frame,(xPos,yPos),ballRadius,ballColor,-1)
    cv2.putText(flipped_frame,str(score),(25,int(6*paddleHeight)),font,6,paddleColor,5)
    cv2.putText(flipped_frame,str(lives),(width-125,int(6*paddleHeight)),font,6,paddleColor,5)
    handData = findHands.Marks(flipped_frame)
    for hand in handData:
        # tip of the index fingure is 8
        # draw a rectangle 
        cv2.rectangle(flipped_frame,(int(hand[8][0]-paddleWidth/2),0),(int(hand[8][0]+paddleWidth/2),paddleHeight),paddleColor,-1)   
    # Game Play 
    topEdgeBall = yPos - ballRadius
    bottomEdgeBall = yPos + ballRadius
    leftEdgeBall = xPos - ballRadius
    rightEdgeBall = xPos + ballRadius
    if leftEdgeBall <= 0 or rightEdgeBall>= width:
        Deltax = Deltax*(-1)
    if bottomEdgeBall >= height:
        Deltay = Deltay*(-1)
    if topEdgeBall <= paddleHeight:
        if xPos >= int(hand[index][0]-paddleWidth/2) and xPos<int(hand[index][0]+paddleWidth/2):
            Deltay = Deltay*(-1)
            score = score+1
            if score==5 or score ==10 or score ==15 or score == 20 or score ==25:
                Deltay = Deltay*2
                Deltax = Deltax*2
        else:
            xPos = int(width/2)
            yPos = int(height/2)
            lives = lives - 1
    xPos = xPos + Deltax
    yPos = yPos + Deltay

    #show the frame 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',0,0)
    if lives == 0:
        break
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
