import cv2
print(cv2.__version__)   

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
                    myHand.append((int(landMark.x * width), int(landMark.y * height)))
                myHands.append(myHand)
        return myHands, handsType

# Setting Up The Camera
width = 1280
height = 720
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

findHands = mpHands(False, 2, .5, .5)

# Game Variables
paddleWidth = 25 
paddleHeight = 125 
paddleColor = (255, 0, 255)
ballRadius = 25
ballColor = (255, 0, 0)
xPos = int(width / 2)
yPos = int(height / 2)
deltaX = 18
deltaY = 18
font = cv2.FONT_HERSHEY_SIMPLEX
fontHeight = 5 
fontWeight = 5
fontColor = (0, 0, 255)
yLeftTip = 0
yRightTip = 0
scoreLeft = 0
scoreRight = 0

while True:
    ignore, frame = cam.read()  
    flipped_frame = cv2.flip(frame, 180)
    flipped_frame = cv2.resize(flipped_frame, (width, height))

    # Ball
    cv2.circle(flipped_frame, (xPos, yPos), ballRadius, ballColor, -1)

    # Scores
    cv2.putText(flipped_frame, str(scoreLeft), (50, 125), font, fontHeight, fontColor, fontWeight)
    cv2.putText(flipped_frame, str(scoreRight), (width - 150, 125), font, fontHeight, fontColor, fontWeight)

    # Detect Hands
    handData, handsType = findHands.Marks(flipped_frame)
    for hand, handType in zip(handData, handsType):
        if handType == 'Left':
            yLeftTip = hand[8][1]  # Left hand index finger tip
        if handType == 'Right':
            yRightTip = hand[8][1]  # Right hand index finger tip

    # Paddle Movement
    cv2.rectangle(flipped_frame, (0, int(yLeftTip - paddleHeight / 2)), (paddleWidth, int(yLeftTip + paddleHeight / 2)), paddleColor, -1)
    cv2.rectangle(flipped_frame, (width - paddleWidth, int(yRightTip - paddleHeight / 2)), (width, int(yRightTip + paddleHeight / 2)), paddleColor, -1)

    # Ball Edges
    topBallEdge = yPos - ballRadius
    bottomBallEdge = yPos + ballRadius
    leftBallEdge = xPos - ballRadius
    rightBallEdge = xPos + ballRadius

    # Ball collision with top and bottom
    if topBallEdge <= 0 or bottomBallEdge >= height:
        deltaY = deltaY * (-1)

    # Ball collision with paddles
    if leftBallEdge <= paddleWidth:
        if yPos >= int(yLeftTip - paddleHeight / 2) and yPos <= int(yLeftTip + paddleHeight / 2):
            deltaX = deltaX * (-1)  # Reverse direction
        else:
            # Right player scores
            scoreRight += 1
            # Reset ball
            xPos = int(width / 2)
            yPos = int(height / 2)

    if rightBallEdge >= width - paddleWidth:
        if yPos >= int(yRightTip - paddleHeight / 2) and yPos <= int(yRightTip + paddleHeight / 2):
            deltaX = deltaX * (-1)  # Reverse direction
        else:
            # Left player scores
            scoreLeft += 1
            # Reset ball
            xPos = int(width / 2)
            yPos = int(height / 2)

    # Update ball position
    xPos += deltaX
    yPos += deltaY

    if scoreLeft+scoreRight >=10:
        break

    # Show the frame
    cv2.imshow('myWEBcam', flipped_frame)
    cv2.moveWindow('myWEBcam', 0, 0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
