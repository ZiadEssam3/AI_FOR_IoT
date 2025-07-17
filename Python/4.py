import cv2
print(cv2.__version__)

rows = int(input('Boss , How Many Rows do You Want? ')) #prompt
columns = int(input('And How Many Columns? '))


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
while True:
    ignore,frame = cam.read()
    #resize frame 
    frame = cv2.resize(frame,(int(width/columns),int(height/columns)))  
    for i in range(0,rows):
        for j in range(0,columns):
           windName = 'window'+str(i)+'x'+str(j)  
           #show window 
           cv2.imshow(windName,frame)
           cv2.moveWindow(windName,int(width/columns)*j,int(height/columns+30)*i)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()