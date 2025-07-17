import cv2 
import numpy as np 
# picture to display 
"""Hue And Saturation"""
x = np.zeros([256,720,3],dtype=np.uint8)
# start generating the color 
for row in range(0,256,1):
    for column in range(0,720,1):
        # modify the x pixel
        # chainging the columns ==> change Hue 
        # chainging the rows    ==> change Saturation 
        # Value            ==> const 255 
        x[row,column] = (int(column/4),row,255) # Hue Saturation 255
x = cv2.cvtColor(x,cv2.COLOR_HSV2BGR)  

"""Hue And Value"""
y = np.zeros([256,720,3],dtype=np.uint8)

# start generating the color 
for row in range(0,256,1):
    for column in range(0,720,1):
        # modify the x pixel
        # chainging the columns ==> change Hue 
        # Saturation            ==> const 255 
        # chainging the rows    ==> change Value 
        y[row,column] = (int(column/4),255,row) # Hue 255 row
y = cv2.cvtColor(y,cv2.COLOR_HSV2BGR)   

while True: 
    cv2.imshow('myHSV',x)
    cv2.moveWindow('myHSV',0,0) # upper left corner
    

    cv2.imshow('myHSV2',y)
    cv2.moveWindow('myHSV2',0,row+40)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cv2.destroyAllWindows()