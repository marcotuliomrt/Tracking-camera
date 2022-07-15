# https://www.youtube.com/watch?v=NZde8Xt78Iw

import cv2
import mediapipe as mp


# loading the holistic module)
mp_holistic = mp.solutions.holistic

# Loaind the function that detects the poses, faces and hands
holistic = mp_holistic.Holistic()

# loading the tools to draw the landmarks once they are detected 
mp_drawing = mp.solutions.drawing_utils


