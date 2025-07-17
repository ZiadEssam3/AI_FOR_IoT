import cv2 
print(cv2.__version__)
import numpy as np 
while True:
    #create numpy array (picture) filled with zero's 
    #gray level picture 
    """frame = np.zeros([250,250],dtype=np.uint8)
    #make picture white 
    #frame[:,:]=255
    #make picture gray 
    #frame[:,:]=125
    # the left tap white , the right is black 
    # frame[:,0:125]=255
    # frame[:,125:250]=255
    # frame[:125,:]=255"""

    #color picture 
    frame = np.zeros([1000,1000,3],dtype=np.uint8)
    frame[:,:]=(0,0,255) #B G R == [0,0,255]
    #make the left half green 
    frame[:,0:500 ]=[0,255,0]
    
    
    #show the picture 
    cv2.imshow('My Window',frame)
    #if the q key is pressed quit 
    if cv2.waitKey(1) & 0xff==ord('q'):
        break
 