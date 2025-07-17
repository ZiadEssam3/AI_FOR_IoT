import cv2
print(cv2.__version__)
import time

#setting the variables
width = 640
height = 360

#rectangle parameters 
upperLeft  = (250,140)
lowerRight = (390,220)
lineWidth = 4

#circle parameters 
myRadius = 30
myColor = (0,0,0)
myThickness = 2

#text parameters 
myText = "Ziad is Boss"
myFont = cv2.FONT_HERSHEY_COMPLEX
fontH = 2
fontT = 2

cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#set window width , height 
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
#set The Frame rate 30 frames per second
cam.set(cv2.CAP_PROP_FPS,10)
#set up the codec 
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

#what time is right now 
tLast = time.time() #LastTime
time.sleep(.1) # to make sure that tLast , time.time() are not the same number
fpsFILT = 10 

while True:
    #How long does it take to go throught the loop
    dT = time.time() - tLast  #change in time dy
    #calculate frames per second 
    fps = 1/dT
    fpsFILT = fpsFILT * .97 + fps* .03 #fps filtered 
    # print(dT)
    print(fps)
    tLast = time.time()


    ignore,frame = cam.read() 
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)


    # old fashion way to do the frame 
    # flipped_frame[140:220,250:390] = (255,0,0)
    # create the rectangle frame using opencv (helper tool cv2) 
    cv2.rectangle(flipped_frame,upperLeft,lowerRight,(0,255,0),lineWidth) # put the cornes
    # create the circle frame using opencv (helper tool cv2) 
    cv2.circle(flipped_frame,(int(width/2),int(height/2)),myRadius,myColor,myThickness )
    # putting text 
    cv2.putText(flipped_frame,myText,(120,125),myFont,fontH,(255,0,0),fontT)
    
    #CREATE RECTANGLE BEHIND THE TEXT
    cv2.rectangle(flipped_frame,(0,0),(130,50),(255,0,255),-1) # put the cornes
    # SHOW TEXT FPS ON THE FRAME
    # cv2.putText(flipped_frame,str(int(fps))+'  fps',(5,30),myFont,1,(0,255,255),2)
    cv2.putText(flipped_frame,str(int(fpsFILT))+'  fps',(5,30),myFont,1,(0,255,255),2)

    # show the frame 
    cv2.imshow('myWEBcam', flipped_frame)
    cv2.moveWindow('myWEBcam',0,0) 
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()