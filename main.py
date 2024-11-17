import cv2
import numpy as py
import json
import os

#sets video cam to default cam -- can be changed
video = cv2.VideoCapture(0)
video.set(3, 640)
video.set(4, 480)

#face recognizer, OpenCVs model
recognizer = cv2.face.LBPHFaceRecognizer_create()
#pull in trainer model file
recognizer.read('trainer.yml')
print(recognizer)

#path for face detection
face_cascade_path = "haarcascade_frontalface_default.xml"
#create a face cascade classifier
faceCascade = cv2.CascadeClassifier(face_cascade_path)

#font
font = cv2.FONT_HERSHEY_SIMPLEX

#converts json file of names to a list that can be referenced later
id = 0
names = ['None']
with open('names.json', 'r') as fs:
    names = json.load(fs)
    names = list(names.values())

#min width and height for window size to be recognized as a face
minW = 0.1 * video.get(3)
minH = 0.1 * video.get(4)

while True:
    #fetch webcam video
    success, img = video.read()
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    

    #Detect any faces
    faces = faceCascade.detectMultiScale(
        gray_image,
        scaleFactor=1.2,
        minNeighbors = 5,
        minSize=(int(minW), int(minH)),
    )

    
    
    for (x, y, w, h) in faces:

        #draws rectangle aroudn the face
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        #predicts user ID and confidence level using recognizer program
        id, confidence = recognizer.predict(gray_image[y:y + h, x:x + w])

        if confidence > 51:
            name = names[id]
            confidence = "  {0}%".format(round(confidence))"
        else:
            name = "Who are you?"
            confidence = "N/A"
        

    #show webcam
    cv2.imshow("webcam", img)

    #stop program when i press q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#once loop is broken stops video and closes window
video.release()
cv2.destroyAllWindows()
