import numpy as np
import json
import cv2
import os

#create a directory to store the photos
def create_directory(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)

#take in the first identifier
def get_face_id(directory: str) -> int:
    user_ids = []
    for filename in os.listdir(directory):
        number = int(os.path.split(filename)[-1].split("-")[1])
        user_ids.append(number)
    user_ids = sorted(list(set(user_ids)))
    max_user_ids = 1 if len(user_ids) == 0 else max(user_ids) + 1
    for i in sorted(range(0, max_user_ids)):
        try:
            if user_ids.index(i):
                face_id = i
        except ValueError as e:
            return i
    return max_user_ids

def save_name(face_id: int, face_name: str, filename: str) -> None:
    names_json = None
    if os.path.exists(filename):
        with open(filename, 'r') as fs:
            names_json = json.load(fs)
    if names_json is None:
        names_json = {}
    names_json[face_id] = face_name
    with open(filename, 'w') as fs:
        json_dump = json.dumps(names_json, ensure_ascii=False, indent=4)
        fs.write(json_dump)

#only run when executed directly
if __name__ == '__main__':
    directory = 'images'
    cascade_classifier_filename = 'haarcascade_frontalface_default.xml'
    names_json_filename = 'names.json'

    # Create 'images' directory if it doesn't exist
    create_directory(directory)
    
    # Load the pre-trained face cascade classifier
    faceCascade = cv2.CascadeClassifier(cascade_classifier_filename)
    
    # connect to cam
    cam = cv2.VideoCapture(0)
    
    # Set camera dimensions
    cam.set(3, 640)
    cam.set(4, 480)
    
    # Initialize face capture variables
    count = 0
    face_name = input('\nEnter user name and press <return> -->  ')
    face_id = get_face_id(directory)
    save_name(face_id, face_name, names_json_filename)
    print('\n[INFO] Initializing face capture. Look at the camera and wait...')

    while True:
        # read frames from cam
        ret, img = cam.read()
    
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        # Detect faces in the frame
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
        # Process each face
        for (x, y, w, h) in faces:
            # Draw a rectangle around the detected face
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
            # Increment the count for naming the saved images
            count += 1

            # Save the captured image into the directory
            cv2.imwrite(f'./images/Users-{face_id}-{count}.jpg', gray[y:y+h, x:x+w])
    
            # Display the image with rectangles around faces
            cv2.imshow('image', img)
    
        # Press escape to cut out of program
        k = cv2.waitKey(100) & 0xff
        if k < 30:
            break
    
        # Take 30 face samples and stop video. You may increase or decrease the number of
        # images. The more, the better while training the model.
        elif count >= 30:
            break
    
    print('\n[INFO] Success! Exiting Program.')
    
    # Release the camera
    cam.release()
    
    # Close all OpenCV windows
    cv2.destroyAllWindows()