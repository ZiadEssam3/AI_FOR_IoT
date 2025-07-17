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
    # Flip the frame Horizontally 
    flipped_frame = cv2.flip(frame, 180)
    frameROI = flipped_frame[150:210,250:390]
    frameROIGray = cv2.cvtColor(frameROI,cv2.COLOR_BGR2GRAY)
    frameROIBGR = cv2.cvtColor(frameROIGray,cv2.COLOR_GRAY2BGR) # (125,125,125) 
    #Show ROI gray frame 
    cv2.imshow('my BGR ROI',frameROIGray)
    cv2.moveWindow('my BGR ROI',650,180)


    #put the gray image back on the color image  
    # becaues the matrix shape matches   
    # flipped_frame[0:60,0:140] = frameROIBGR
    flipped_frame[0:60,0:140] = frameROI
    
    
    #Show ROI gray frame 
    cv2.imshow('my Gray ROI',frameROIGray)
    cv2.moveWindow('my Gray ROI',650,90)
    #Show ROI frame 
    cv2.imshow('my ROI',frameROI)
    cv2.moveWindow('my ROI',650,0)


    #show the frame 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',0,0)


    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()