import cv2
print(cv2.__version__)
import mediapipe as mp 
print(mp.__version__)

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

# face object 
faceMesh = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=False,          # Whether to treat the input image as a static image (True) or a video stream (False)
    max_num_faces=3,                  # Maximum number of faces to detect in the image (3 in your case)
    min_detection_confidence=0.5,     # Minimum confidence threshold for face detection (0.5)
    min_tracking_confidence=0.5       # Minimum confidence threshold for face landmark tracking (0.5)
)
# drawing object 
mpDraw = mp.solutions.drawing_utils
font = cv2.FONT_HERSHEY_SIMPLEX
fontSize = .4
fontColor = (0,255,255)
fontThick = 1 

drawSpecCircle = mpDraw.DrawingSpec(thickness = 3,circle_radius = 2,color = (0,0,0))
drawSpecLine   = mpDraw.DrawingSpec(thickness = -1,circle_radius = 3,color=(0,0,255))

while True:
    ignore,frame = cam.read()  
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    flipped_frame = cv2.resize(flipped_frame,(width,height))
    # make the fram in rgb color space to send to mediapipe 
    frameRGB = cv2.cvtColor(flipped_frame,cv2.COLOR_BGR2RGB)
    results = faceMesh.process(frameRGB)
    # print(results.multi_face_landmarks)
    # that prints 468 data points for each frame 
    # each point is got like landmark x , y , z
    """
    landmark {
        x: 0.514767349
        y: 0.327409804
        z: -0.0271908939
    } 
    """
    # do things 
    if results.multi_face_landmarks != None:
        # step throw faces 
        for faceLandmarks in results.multi_face_landmarks:
            mpDraw.draw_landmarks(
                flipped_frame,
                faceLandmarks,
                mp.solutions.face_mesh.FACEMESH_TESSELATION,
                drawSpecLine,
                drawSpecCircle
            )
            indx = 0
            for lm in faceLandmarks.landmark:
                cv2.putText(flipped_frame,str(indx),(int(lm.x*width),int(lm.y*height)),font,fontSize,fontColor,fontThick)
                indx = indx+1

    #show the frame 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()