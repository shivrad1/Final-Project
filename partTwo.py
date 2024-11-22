import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import json

# Function to initialize face recognition
def load_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    trainer_path = "trainer.yml"
    if os.path.exists(trainer_path):
        recognizer.read(trainer_path)
    else:
        print("Trainer file not found!")
        exit()
    return recognizer

# Function to load names from JSON file
def load_names():
    names = {}
    if os.path.exists('names.json'):
        with open('names.json', 'r') as file:
            names = json.load(file)
    return names

# Function to initialize face detection
def initialize_face_detector():
    face_cascade_path = "haarcascade_frontalface_default.xml"
    if os.path.exists(face_cascade_path):
        return cv2.CascadeClassifier(face_cascade_path)
    else:
        print("Haar cascade file not found!")
        exit()

# Function to capture a single image, recognize face, and return name
def capture_and_identify(ui_label, ui_image_label, password_entry_frame, capture_button_frame):
    global name
    # Open the webcam
    video = cv2.VideoCapture(0)
    face_cascade = initialize_face_detector()
    recognizer = load_recognizer()
    names = load_names()
    
    # Capture one frame (take a picture)
    success, img = video.read()
    if not success:
        messagebox.showerror("Error", "Failed to capture image.")
        return

    # Convert image to grayscale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))

    # If no faces, return error message
    if len(faces) == 0:
        messagebox.showwarning("No Face Detected", "Please position your face in front of the camera.")
        video.release()
        return
    
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Predict the user ID and confidence
        user_id, confidence = recognizer.predict(gray_image[y:y+h, x:x+w])
        
        if confidence < 100:
            name = names.get(str(user_id), "Unknown")
            ui_label.config(text=f"Hello, {name}!")
            print(confidence)
        else:
            ui_label.config(text="Unknown User")
        
    # Convert the captured image to a format Tkinter can display
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
    img_pil = Image.fromarray(img_rgb)  # Convert to PIL image
    img_tk = ImageTk.PhotoImage(img_pil)  # Convert to Tkinter image format
    
    # Update the image label to show the captured image
    ui_image_label.config(image=img_tk)
    ui_image_label.image = img_tk  # Keep a reference to the image to prevent garbage collection
    
    # Release the webcam
    video.release()

    # Schedule removal of image after 10 seconds and show password entry
    def show_password_entry():
        ui_image_label.config(image='')  # Clear the image
        ui_label.config(text="Enter your password below:")

        # Remove the capture button and add a go back button
        for widget in capture_button_frame.winfo_children():
            widget.destroy()

        go_back_button = tk.Button(capture_button_frame, text="Go Back", font=("Helvetica", 12), command=go_back)
        go_back_button.pack(pady=10)

        # Create and display the password entry widget
        password_label = tk.Label(password_entry_frame, text="Password:", font=("Helvetica", 12))
        password_label.grid(row=0, column=0, padx=20, pady=10)

        password_entry = tk.Entry(password_entry_frame, font=("Helvetica", 12), show="*")
        password_entry.grid(row=0, column=1, padx=20, pady=10)

        submit_button = tk.Button(password_entry_frame, text="Submit", font=("Helvetica", 12), command=lambda: check_password(password_entry.get()))
        submit_button.grid(row=1, columnspan=2, pady=10)

    # Call show_password_entry after 5 seconds
    window.after(5000, show_password_entry)

# Function to check the entered password
def check_password(password):
    global name
    ben_password = "1234"
    shiv_password = "4321"
    if password == ben_password and name == 'Ben':
        messagebox.showinfo("Success", "Password accepted!")
    elif password == shiv_password and name == 'Shiv':
        messagebox.showinfo("Success", "Password accepted!")
    else:
        messagebox.showerror("Error", "Incorrect password.")

# Function to go back to the initial state
def go_back():
    ui_label.config(text="Welcome! Please position your face in front of the camera.")
    for widget in password_entry_frame.winfo_children():
        widget.destroy()
    for widget in capture_button_frame.winfo_children():
        widget.destroy()

    start_button = tk.Button(capture_button_frame, text="Capture and Recognize", font=("Helvetica", 12), command=lambda: capture_and_identify(ui_label, ui_image_label, password_entry_frame, capture_button_frame))
    start_button.pack(pady=20)

# Function to start the UI
def start_ui():
    global window  # Declare window as global to use it inside other functions
    global ui_label, ui_image_label, password_entry_frame, capture_button_frame 
    window = tk.Tk()
    window.title("Face Recognition System")

    # Instructions for the user
    ui_label = tk.Label(window, text="Welcome! Please position your face in front of the camera.", font=("Helvetica", 14))
    ui_label.pack(pady=20)

    # Label to display the captured image
    ui_image_label = tk.Label(window)
    ui_image_label.pack(pady=20)

    # Frame for password entry
    password_entry_frame = tk.Frame(window)
    password_entry_frame.pack(pady=20)

    # Frame for capture and Go Back button
    capture_button_frame = tk.Frame(window)
    capture_button_frame.pack(pady=20)

    # Button to start capturing image for recognition
    start_button = tk.Button(capture_button_frame, text="Capture and Recognize", font=("Helvetica", 12), command=lambda: capture_and_identify(ui_label, ui_image_label, password_entry_frame, capture_button_frame))
    start_button.pack(pady=20)

    # Start the GUI loop
    window.mainloop()

# Starts the program
if __name__ == "__main__":
    start_ui()
