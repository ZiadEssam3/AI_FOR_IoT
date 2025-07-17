import cv2 
import face_recognition as FR 
# labeling pictures 
font = cv2.FONT_HERSHEY_SIMPLEX 
# train of 2 faces 
""" Load Up a Known image """
donFace = FR.load_image_file('C:/Users/ziade/Documents/Python/DemoImages/known/Donald Trump.jpg')
""" 1) Find A Face in the Image"""
faceLoc = FR.face_locations(donFace)[0]
""" 2) Encode The Face """
doneFaceEncode = FR.face_encodings(donFace)[0]

nancyFace = FR.load_image_file('C:/Users/ziade/Documents/Python/DemoImages/known/Nancy Pelosi.jpg')
faceLoc = FR.face_locations(nancyFace)[0]
nancyFaceEncode = FR.face_encodings(nancyFace)[0]

penceFace = FR.load_image_file('C:/Users/ziade/Documents/Python/DemoImages/known/Mike Pence.jpg')
faceLoc = FR.face_locations(penceFace)[0]
penceFaceEncode = FR.face_encodings(penceFace)[0]


knownEncodings = [doneFaceEncode,nancyFaceEncode,penceFaceEncode]
names = ['Donal Trump','Nancy Pelosi','Mike Pence']


unknownFace = FR.load_image_file('C:/Users/ziade/Documents/Python/DemoImages/unknown/u1.jpg')
unknownFaceBGR = cv2.cvtColor(unknownFace,cv2.COLOR_RGB2BGR)
faceLocations = FR.face_locations(unknownFace)
unknownEncodings = FR.face_encodings(unknownFace,faceLocations)

for faceLocation,unknownEncoding in zip(faceLocations,unknownEncodings):
    top,right,bottom,left = faceLocation
    print(faceLocation)
    cv2.rectangle(unknownFaceBGR,(left,top),(right,bottom),(255,0,0),3)
    name = 'Unknown Person'
    matches = FR.compare_faces(knownEncodings,unknownEncoding)
    print(matches)
    if True in matches:
        matchIndex = matches.index(True)
        print(matchIndex)
        print(names[matchIndex])
        name = names[matchIndex]
    cv2.putText(unknownFaceBGR,name,(left,top),font,.8,(0,255,0),2)

cv2.imshow('MyFaces',unknownFaceBGR)
cv2.waitKey(5000)


"""print(faceLoc) 
# [(266, 464, 489, 241)] # [(top, right, bottom, left)]
top,right,bottom,left = faceLoc
cv2.rectangle(donFace,(left,top),(right,bottom),(255,0,0),1)
donFaceBGR  = cv2.cvtColor(donFace,cv2.COLOR_RGB2BGR)"""
# cv2.imshow('MyWindow',donFaceBGR)
# cv2.waitKey(5000)