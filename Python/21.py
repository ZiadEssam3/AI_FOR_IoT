import cv2
print(cv2.__version__)
"""*******************Setting Up The Camera ******************"""
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
"""******************* Setting Up The FaceRecogiizer ******************"""
# this is a model that has been trained to identify the faces probably we take object of it to use   
# create an Object
# give it the path of tha cascade i want
"""Relative Path"""  
faceCascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')
"""Absolute Path"""
# faceCascade = cv2.CascadeClassifier('C:\Users\ziade\Documents\Python\haar\haarcascade_frontalface_default.xml')
 

while True:
    ignore,frame = cam.read()  
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    frameGray = cv2.cvtColor(flipped_frame,cv2.COLOR_BGR2GRAY)
    # find the faces 
    faces = faceCascade.detectMultiScale(frameGray,1.3,5)
    # print(faces) # to now the returned data structure 
    
    # Put a box around the face found but it may alot of face found 
    # step throw the face positions 
    for face in faces:
      x,y,w,h = face 
      # make shure the grapping of this values out of the array 
      #print('x=',x,'y=',y,'width=',w,'height=',h)
      cv2.rectangle(flipped_frame,(x,y),(x+w,y+h),(255,0,0),2) 
    #show the frame 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()