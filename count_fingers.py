import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# loading detection accuracy percentage
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

# taking the tip landmarks of all 5 fingers
tipIds = [4, 8, 12, 16, 20]

# Define a function to count fingers
def countFingers(image, hand_landmarks, handNo=0):
    print()

    if hand_landmarks:
        landmark = hand_landmarks[handNo].landmark
        fingers = []

        for landmark_index in tipIds:
            fingertip_y = landmark[landmark_index].y
            fingerbottom_y = landmark[landmark_index-2].y

            fingertip_x = landmark[landmark_index].x
            fingerbottom_x = landmark[landmark_index-2].x

            if landmark_index != 4:
                if fingertip_y < fingerbottom_y:
                    fingers.append(1)
                    print("finger ", landmark_index, "is up")

                if fingertip_y > fingerbottom_y:
                    fingers.append(0)
                    print("finger ", landmark_index, "is not up")
            else:
                if fingertip_x > fingerbottom_x:
                    fingers.append(1)
                    print("finger ", landmark_index, "is up")
                
                if fingertip_x < fingerbottom_x:
                    fingers.append(0)
                    print("finger", landmark_index, "is not up")
        
        total_fingers = fingers.count(1)
        print('total_fingers=', total_fingers)
        
        text = f'Fingers: {total_fingers}'
        cv2.putText(image, text, (200, 50), cv2.FONT_HERSHEY_PLAIN, 5, (100, 0, 0), 5)

# Define a function to 
def drawHandLanmarks(image, hand_landmarks):

    # Darw connections between landmark points
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)


while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detect the Hands Landmarks 
    results = hands.process(image)

    # Get landmark position from the processed result
    hand_landmarks = results.multi_hand_landmarks

    # Draw Landmarks
    drawHandLanmarks(image, hand_landmarks)

    # Get Hand Fingers Position        
    countFingers(image, hand_landmarks)

    cv2.imshow("Media Controller", image)

    # Quit the window on pressing Sapcebar key
    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()
