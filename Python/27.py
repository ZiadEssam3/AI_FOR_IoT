import cv2 
print(cv2.__version__)
import face_recognition as FR 
import pickle
# labeling pictures 
font = cv2.FONT_HERSHEY_SIMPLEX 
"""Setting up the Camera """
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


# names = ['Ziad Essam','Cristiano Ronaldo']
# knownEncodings = [ziadFaceEncode,CR7FaceEncode]
with open('Train/train2.pkl','rb') as f:
    names = pickle.load(f)
    knownEncodings = pickle.load(f)



while True:
    ignore,unknownFace = cam.read()
    # Flip the frame Horizontally 
    flipped_unknownFace = cv2.flip(unknownFace, 180)
    unknownFaceRGB = cv2.cvtColor(flipped_unknownFace,cv2.COLOR_RGB2BGR)
    faceLocations = FR.face_locations(unknownFaceRGB)
    unknownEncodings = FR.face_encodings(unknownFaceRGB,faceLocations)

    for faceLocation,unknownEncoding in zip(faceLocations,unknownEncodings):
        top,right,bottom,left = faceLocation
        print(faceLocation)
        cv2.rectangle(flipped_unknownFace,(left,top),(right,bottom),(255,0,0),3)
        name = 'Unknown Person'
        matches = FR.compare_faces(knownEncodings,unknownEncoding)
        print(matches)
        if True in matches:
            matchIndex = matches.index(True)
            print(matchIndex)
            print(names[matchIndex])
            name = names[matchIndex]
        cv2.putText(flipped_unknownFace,name,(left,top),font,.8,(0,255,0),2)

    cv2.imshow('MyFaces',flipped_unknownFace)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()