# https://www.youtube.com/watch?v=NZde8Xt78Iw

import cv2
import mediapipe as mp
import time
import serial.tools.list_ports
import numpy as np

# --------------------------     arguments      --------------------------------------------------------------

x_cam = 640
y_cam = 460
sections = 10

# Precision: fraction of the screen size that the object been tracked can move without activating the camera movement
x_precision = 0.6
y_precision = 0.6


# ---------------------------    serial port: python -> c++     ----------------------------------------------
port = "/dev/ttyUSB0" # adapter
# port = "/dev/ttyACM0" # arduino

ser = serial.Serial(port)
print("port: "+port)
ser.baudrate=115200


# ---------------------------     frame sections        ------------------------------------------------------

buffer_x = [5,5]
buffer_y = [5,5]

# x_intervals_list = [int(i) for i in np.arange(0, x_cam, x_cam/sections)] + [x_cam]
# y_intervals_list = [int(i) for i in np.arange(0, y_cam, y_cam/sections)] + [y_cam]
# function that get the intervals of the index finger tip
# def get_interval(coordinates, x_inter = x_intervals_list, y_inter = y_intervals_list):
#     # gets the x and y coordenates of the hand
#     x, y = coordinates
#     # iterates over the x intervals
#     for i in range(len(x_inter)):
#         # if the x coordenate is between the interval
#         if x > x_inter[i] and x < x_inter[i+1]:
#             # gets the x interval
#             x_interval = i


#             # iterates over the x intervals
#             for j in range(len(y_inter)):
#                 # if the y coordenate is between the interval
#                 if y > y_inter[j] and y < y_inter[j+1]:
#                     # gets the y interval
#                     y_interval = j

#                     interval = [x_interval, y_interval]

#     return interval
          
 
#   9 8 7 6 5 4 3 2 1 0
#                      0
#                      1
#                      2
#        screen        3
#       intervals      4
#        matrix        5
#                      6
#                      7
#                      8
#                      9




x_intervals_list = [int(i+ x_cam/sections) for i in np.arange(0, x_cam, x_cam/sections)]
y_intervals_list = [int(i+ y_cam/sections) for i in np.arange(0, y_cam, y_cam/sections)]

def get_interval(coordinates, x_inter = x_intervals_list, y_inter = y_intervals_list):
    # gets the x and y coordenates of the hand
    x, y = coordinates
    # iterates over the x intervals
    for i in range(len(x_inter)):
        if x <= x_inter[i]:
            # gets the x interval
            x_interval = i
            break


    # iterates over the x intervals
    for j in range(len(y_inter)):
        # if the y coordenate is between the interval
        if y <= y_inter[j]:
            # gets the y interval
            y_interval = j
            break
    #    list variable
    #interval = [x_interval, y_interval]
    #    concatenated variable to send both coorsinates simultaneously to the serial
    # interval = int(str(x_interval) + str(y_interval))

    # Obs: the var "interval" must be a list, otherwise it apears just zeros on the serial monitor of the ardiuno
    return [x_interval, y_interval]
          

          

# ---------------------------- function that gets the coordinates --------------------------------
def main_func():
    # create the VIdeoCapture object from the webcam
    # obs: 0: integrates webcam, 2: usb camera
    cap = cv2.VideoCapture(0)

    # getting the 
    mphands = mp.solutions.hands
    # objects hand
    hands = mphands.Hands()
    # function that draws landmarks and its lines
    lms_drawer = mp.solutions.drawing_utils 

    c_time = 0
    p_time = 0

    while True:
        # get the frame
        bool, frame = cap.read()
        # convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # gets the hight, width and num of chanels of the frame
        h, w, c = frame.shape

        # gets the curent time
        c_time = time.time()
        # gets the fps
        fps = 1/(c_time - p_time)
        # set the previous time equlas to the current time 
        p_time = c_time

        # displays the fps on the screen 
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    
        # detect a hand (True if detects at least one)
        if results.multi_hand_landmarks:
            # iterates over the any detected hands
            for hand_id, hand_lms in enumerate(results.multi_hand_landmarks):
                # draw the landmarks and the lines between on the hands
                lms_drawer.draw_landmarks(frame, hand_lms, mphands.HAND_CONNECTIONS, 
                            lms_drawer.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
                            lms_drawer.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                            )
                                
                # gets and iterates the id and coordenates (in % of the screen) of each landmark 
                for finger_id, lm in enumerate(hand_lms.landmark):
                    # gets the coordenates of the landmark in PIXELS
                    wp, hp = int(lm.x * w), int(lm.y * h)
                    current_lm = [hand_id, finger_id, wp, hp]

                    # obs: the index finger tip is the landmark with the id = 8
                    if current_lm[1] == 8:
        
                        # gets just the coordenates of the index finger tip
                        # OBS: If the value of the x coordinate is 0 it doens't apear on the variable xy because its on the left of the number 
                        xy = current_lm[2:]
                        # gets the intervals in the acreen of the finget tip
                        intervals = get_interval(xy)
                        #print(xy)
                        #print(intervals)
                        
                        del buffer_x[0] # removes the first element of the x list
                        buffer_x.append(intervals[0]) # adds the new value to the last x list position
                        del buffer_y[0] # removes the first element of the y list
                        buffer_y.append(intervals[1]) # adds the new value to the last y list position



                        if (abs(5 - buffer_x[1]) >= (1 - x_precision)*sections/2) | (abs(5 - buffer_y[1]) >= (1 - y_precision)*sections/2):
                            # Sends the coordinates to the serial port
                            ser.write(intervals)
                            print(intervals)
                                                    
                            

                        



        # set the condition of manual brake by pressing "q" on the keyboard  
        if cv2.waitKey(1) & 0xFF==ord("k"):
            break


        cv2.imshow("Test video", frame)
        cv2.waitKey(1)

    # release the webcam 
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main_func()

