import cv2
import mediapipe as mp 
print(cv2.__version__)
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

# pos detection object : allow us to analyze body to find the landmarks  
pose = mp.solutions.pose.Pose(
    static_image_mode=False,
    model_complexity=False,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
# Draw The results 
mpDraw = mp.solutions.drawing_utils

circleRadius = 10 
circleColor = (0,0,255)
circleThickness = 4
eyeColor = (255,0,0)
eyeRadius = 10
eyeThickness = 1
while True:
    ignore,frame = cam.read()  
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    flipped_frame = cv2.resize(flipped_frame,(width,height))
    frameRGB = cv2.cvtColor(flipped_frame,cv2.COLOR_BGR2RGB)
    # analyze the frame 
    # results : datastructure that the data comes back in 
    results = pose.process(frameRGB)
    # print(results)
    landMarks = []
    if results.pose_landmarks != None:
        # mpDraw.draw_landmarks(flipped_frame,results.pose_landmarks,mp.solutions.pose.POSE_CONNECTIONS)
        # print(results.pose_landmarks)
        """
        landmark {
            x: 0.401223898
            y: 3.39020014
            z: 0.000463193835
            visibility: 0.0191697646
        }
        """
        # step throw the landmarks 
        for lm in results.pose_landmarks.landmark:
           # print((lm.x,lm.y))
           landMarks.append((int(lm.x*width),int(lm.y*height)))
        print(landMarks)
        
        cv2.circle(flipped_frame,landMarks[0],circleRadius,circleColor,circleThickness)
        cv2.circle(flipped_frame,landMarks[2],eyeRadius,eyeColor,eyeThickness)
        cv2.circle(flipped_frame,landMarks[5],eyeRadius,eyeColor,eyeThickness)

        # for index in range(0,31,1):
            # cv2.circle(flipped_frame,landMarks[index],circleRadius,circleColor,circleThickness)
    #show the frame 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()