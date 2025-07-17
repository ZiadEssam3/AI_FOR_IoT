#Checkerboard 
import cv2 
print(cv2.__version__)
import numpy as np 

boardSize  = int(input('What size is your Board Boss? '))
numSquares = int(input('And Sir , How Many Squares? '))
squareSize = int(boardSize/numSquares) 

darkColor  = (0,0,0)
lightColor = (175,255,175)
nowColor   = darkColor

#create infinte loop
while True:
    #create a picture with numpy array
    x = np.zeros([boardSize,boardSize,3],dtype=np.uint8)
    #put the squares 
    for row in range(0,numSquares):
        for col in range(0,numSquares):
            #the magic is happens making slicing 
            x[squareSize*row:squareSize*(row+1),squareSize*col:squareSize*(col+1)] = nowColor   
            if nowColor == darkColor:
                nowColor = lightColor
            else:
                nowColor = darkColor
        #reflip 
        if nowColor == darkColor:
            nowColor = lightColor
        else:
            nowColor = darkColor
    #show the frame 
    cv2.imshow('My Checkerboard',x)
    #exit program by pressing q 
    if cv2.waitKey(1) & 0xff==ord('q'):
        break


