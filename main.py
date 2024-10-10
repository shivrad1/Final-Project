import cv2
import numpy as py

#sets video cam to default cam -- can be changed
video = cv2.VideoCapture(0)

while True:
    #fetch webcam video
    success, img = video.read()
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #show webcam
    cv2.imshow("webcam", img)

    #stop program when i press q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#once loop is broken stops video and closes window
video.release()
cv2.destroyAllWindows()
