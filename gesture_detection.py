
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model


# up: thumbs up
# down: thumbs down
# right: peace
# left: okay
# stop: stop
class GestureRecognition():
    mpHands = mp.solutions.hands
    hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mpDraw = mp.solutions.drawing_utils
    model = load_model('mp_hand_gesture')
    def __init__(self,manager):
        with open('gesture.names', 'r') as f:
            self.classNames = f.read().split('\n')

        self.manager=manager
    
    def start_video_cap(self):
        self.cap=cv2.VideoCapture(0)
    def processing_loop(self):
        while True:
            _, frame = self.cap.read()

            x, y, c = frame.shape

            # Flip the frame vertically
            frame = cv2.flip(frame, 1)
            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get hand landmark prediction
            result = self.hands.process(framergb)
        
            className = ''

            if result.multi_hand_landmarks:
                landmarks = []
                for handslms in result.multi_hand_landmarks:
                    for lm in handslms.landmark:
                        # print(id, lm)
                        lmx = int(lm.x * x)
                        lmy = int(lm.y * y)

                        landmarks.append([lmx, lmy])

                    # Drawing landmarks on frames
                    self.mpDraw.draw_landmarks(frame, handslms, self.mpHands.HAND_CONNECTIONS)

                    # Predict gesture
                    prediction = self.model.predict([landmarks])
                    # print(prediction)
                    classID = np.argmax(prediction)
                    className = self.classNames[classID]
                    print(className)
                    if className!='':
                        self.manager['0']=className

            # show the prediction on the frame
            cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0,0,255), 2, cv2.LINE_AA)
            cv2.imshow("Output", frame) 

            if cv2.waitKey(1) == ord('q'):
                break
    def exit_processing(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def start_gesture_detection(self):
        self.start_video_cap()
        self.processing_loop()
        self.exit_processing()


def start_recognition(manager):
    x=GestureRecognition(manager)
    x.start_gesture_detection()