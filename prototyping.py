import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load the gesture recognizer model
model = load_model('mp_hand_gesture')
# Load class names
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)

# Initialize the webcam for Hand Gesture Recognition Python project
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    x, y, c = frame.shape
  # Flip the frame vertically
    frame = cv2.flip(frame, 1)
  # Show the final output
    cv2.imshow("Output", frame)
    if cv2.waitKey(1) == ord('q'):
        break
# release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()