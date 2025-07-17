import cv2
print(cv2.__version__)
import mediapipe as mp 

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

# create an object that allow us to find faces 
findFace = mp.solutions.face_detection.FaceDetection()
# use the drawing utility 
drawFace = mp.solutions.drawing_utils

while True:
    ignore,frame = cam.read()  
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    flipped_frame = cv2.resize(flipped_frame,(width,height))
    frameRGB = cv2.cvtColor(flipped_frame,cv2.COLOR_BGR2RGB)
    # find some faces 
    results = findFace.process(frameRGB)
    print(results.detections)
    if results.detections != None: # means it found a face 
        for face in results.detections:
            # canned routine of draw faces with mediapipe 
            # drawFace.draw_detection(flipped_frame,face)
            bBox = face.location_data.relative_bounding_box
            topLeft = (int(bBox.xmin*width),int(bBox.ymin*height))
            bottomRight = (int((bBox.xmin+bBox.width)*width),int((bBox.ymin+bBox.height)*height))
            # draw rectangle with opencv 
            cv2.rectangle(flipped_frame,topLeft,bottomRight,(255,0,0),3)

    """
    [label_id: 0
        score: 0.980437458
        location_data {
        format: RELATIVE_BOUNDING_BOX
        relative_bounding_box {
            xmin: 0.341306448
            ymin: 0.356310368
            width: 0.258183241
            height: 0.458992302
    }
    """

    #show the frame 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()