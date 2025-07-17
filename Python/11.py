import cv2
print(cv2.__version__)
evt = 0 # make the program not craches 
def mouseClick(event,xPos,yPos,flags,params):
    global evt
    global pnt
    #sence pick up or down a left click 
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Mouse Event was: ',event)
        print('at Position',xPos,yPos)
        pnt = (xPos,yPos)
        evt = event

    if event == cv2.EVENT_LBUTTONUP:
        print('Mouse Event was: ',event)
        print('at Position',xPos,yPos)
        evt = event
    #sence pick up or down a right click 
    if event == cv2.EVENT_RBUTTONUP:
        # to know the event number
        print('Right Button Up: ',event)
        pnt = (xPos,yPos)
        evt = event


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

#creating the window that we are going to be using down 
# i tell the program that i have window called .....
cv2.namedWindow('myWEBcam')
#make listner to events 
cv2.setMouseCallback('myWEBcam',mouseClick)

while True:
    ignore,frame = cam.read()  
    flipped_frame = cv2.flip(frame, 180)

    
    if evt == 1 or evt == 4:
        #put circel 
        cv2.circle(flipped_frame,pnt,25,(255,0,0),2)

    
    #show the frame in my main window 
    cv2.imshow('myWEBcam',flipped_frame)
    cv2.moveWindow('myWEBcam',0,0) 
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()