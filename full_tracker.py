# https://www.youtube.com/watch?v=NZde8Xt78Iw

import cv2
import mediapipe as mp


# loading the holistic module)
mp_holistic = mp.solutions.holistic

# Loaind the function that detects the poses, faces and hands
holistic = mp_holistic.Holistic()

# loading the tools to draw the landmarks once they are detected 
mp_drawing = mp.solutions.drawing_utils



cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    
    # convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Pass the image through the model -> make Detections
    results = holistic.process(rgb_frame)

    # Recolor image back to BGR for rendering
    bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

    # Draw face landmarks
    mp_drawing.draw_landmarks(bgr_frame, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
                                 mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                 mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                 )
    # 4. Pose Detections
    mp_drawing.draw_landmarks(bgr_frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                 mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                 )

    cv2.imshow('frame', bgr_frame)
   

    if cv2.waitKey(10) & 0xFF == ord('k'):
        break

cap.release()
cv2.destroyAllWindows()