import cv2
print(cv2.__version__)
#setting the variables
width = 640
height = 360
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
    cv2.imshow('myWEBcam',frame)
    cv2.moveWindow('myWEBcam',0,0) 
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()