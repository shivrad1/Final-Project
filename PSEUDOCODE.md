PSEUDOCODE

1. **Setup**
    - Install OpenCV if not already installed:
        - Run `pip install opencv-python`

2. **Import OpenCV Library**
    - Import OpenCV: `import cv2`

3. **Load Image**
    - Load the image file:
        - `img = cv2.imread('input_image.jpg')`

4. **Convert to Grayscale**
    - Convert the image to grayscale (needed for face detection):
        - `gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`

5. **Load Face Classifier**
    - Load the pre-trained face detection model:
        - `face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')`

6. **Detect Faces**
    - Detect faces in the grayscale image:
        - `faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)`

7. **Draw Bounding Boxes Around Faces**
    - For each detected face, draw a rectangle:
        - Loop through `faces` and draw rectangles on `img` for each face position.

8. **Display the Image with Faces Highlighted**
    - Display the result:
        - `cv2.imshow('Face Detection', img)`
    - Wait for a key press to close the window:
        - `cv2.waitKey(0)`
        - `cv2.destroyAllWindows()`
