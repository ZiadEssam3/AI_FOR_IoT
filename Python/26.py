import os 
import cv2 
import face_recognition as FR 
import pickle # our old friend ^_^
print(cv2.__version__)
# array of our training data 
encodings = []
names = []
# tell it where to start where our images (known) are 
imageDir = 'C:\\Users\ziade\Documents\Python\DemoImages\known'
# walk throw the folder (how we walk ? ==> we walk throw imageDir)
for root,dirs,files in os.walk(imageDir):
  print(root)
  print(dirs)
  print(files)
  # step throw files 
  for file in files:
    # print(file)
    # join the filename with the path name 
    fullFilePath = os.path.join(root,file)
    print(fullFilePath)
    # load the image 
    myPicture = FR.load_image_file(fullFilePath)
    # encode the image 
    encoding= FR.face_encodings(myPicture)[0]
    # person's name 
    name = os.path.splitext(file)[0]
    encodings.append(encoding)
    names.append(name)
# pickle the data 
with open('Train/train2.pkl','wb') as f:
  pickle.dump(names,f)
  pickle.dump(encodings,f)
