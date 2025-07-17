import os # give tools to walk throw file structure 
import cv2 
import face_recognition as FR 
print(cv2.__version__)
# where i want to start 
imageDir = 'C:\\Users\ziade\Documents\Python\DemoImages\known'

for root,dirs,files in os.walk(imageDir):
    print('MyWorking Folder(root):',root)
    print('dirs in root: ',dirs)
    print('My Files in root:',files)
    for file in files:
        print('Your Gut is:',file)
        fullFilePath = os.path.join(root,file)
        print(fullFilePath)
        # get persons name without extention 
        name = os.path.splitext(file)[0]
        print(name)
        myPicture = FR.load_image_file(fullFilePath)
        myPicture = cv2.cvtColor(myPicture,cv2.COLOR_RGB2BGR)
        cv2.imshow(name,myPicture)
        cv2.moveWindow(name,0,0)
        cv2.waitKey(2500)
        cv2.destroyAllWindows()

