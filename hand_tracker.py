# https://www.youtube.com/watch?v=NZde8Xt78Iw

import cv2
import mediapipe as mp
import time
import serial.tools.list_ports
import numpy as np

# ----------------------------     arguments      ------------------------------------------------------------

x_cam = 640  # image width
y_cam = 460  # image lengh 

# OBS: always use a odd number
sections = 11 # number of sections the image is being devided (the resolution the the tracking)

# Precision: fraction of the screen size that the object been tracked can move without activating the camera movement
x_precision = 0.5
y_precision = 0.5

# ---------------------------    calculated variables --------------------------------------------------------


x_intervals_list = [int(i+ x_cam/sections) for i in np.arange(0, x_cam, x_cam/sections)]
y_intervals_list = [int(i+ y_cam/sections) for i in np.arange(0, y_cam, y_cam/sections)]

# for sections = 10
# x_intervals_list = [64, 128, 192, 256, 320, 384, 448, 512, 576, 640]
# y_intervals_list = [46, 92, 138, 184, 230, 276, 322, 368, 414, 460]

x_prec_interval = (1 - x_precision)*sections/2
y_prec_interval = (1 - y_precision)*sections/2

# for x_precision = x_precision = 0.6 and sections = 10
# x_prec_interval = x_prec_interval = 2

x_section_size = x_intervals_list[0]
y_section_size = y_intervals_list[0]

x0 = int(x_cam/2 - x_prec_interval*x_section_size)
x1 = int(x_cam/2 + x_prec_interval*x_section_size)
y0 = int(y_cam/2 - y_prec_interval*y_section_size)
y1 = int(y_cam/2 + y_prec_interval*y_section_size)


# ---------------------------    serial port: python -> c++     ----------------------------------------------
port = "/dev/ttyUSB0" # USB-TTL adapter
# port = "/dev/ttyACM0" # arduino

ser = serial.Serial(port)
print("port: "+port)
ser.baudrate= 9600

# ---------------------------     func that sends the data   -------------------------------------------------

# sends the data and prints on the terminal
def serial_send(data):
    data = data.encode('ascii')
    print(data)
    ser.write(data)
    time.sleep(0.05)


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
    
    # Code to use with arduino
    interval = int(str(x_interval) + str(y_interval))  # concatenated variable to send both coorsinates simultaneously to the serial
    # Obs: the var "interval" must be a list, otherwise it apears just zeros on the serial monitor of the ardiuno
    # return [interval]

    # # Code to use with st nucleo
    return [x_interval, y_interval, [interval]]

          




# ---------------------------- function that gets the coordinates --------------------------------
def main_func():
    
    # obs: 0: integrates webcam, 2: usb camera
    cap = cv2.VideoCapture(0)  # create the VIdeoCapture object from the webcam

    
    mphands = mp.solutions.hands  # getting the  ???
    hands = mphands.Hands()  # objects hand
    lms_drawer = mp.solutions.drawing_utils  # function that draws landmarks and its lines

    c_time = 0  # current time
    p_time = 0  # previous time

    while True:
        
        bool, frame = cap.read()  # get the frame

        # convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        h, w, c = frame.shape  # gets the hight, width and num of chanels of the frame
        
        c_time = time.time()  # gets the curent time
        fps = 1/(c_time - p_time)  # gets the fps         
        p_time = c_time  # set the previous time equlas to the current time 

        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)  # displays the fps on the screen 
        
    
        # loops that draw the grid
        for i in y_intervals_list:  # loop to draw all lines parallel to the x axis
            cv2.line(img=frame, pt1=(0, i), pt2=(x_cam, i), color=(255, 0, 0), thickness=1, lineType=8, shift=0)  # line in the x axis

        for j in x_intervals_list:  # loop to draw all lines parallel to the y axis
            cv2.line(img=frame, pt1=(j, 0), pt2=(j, y_cam), color=(255, 0, 0), thickness=1, lineType=8, shift=0)  # line in the y axis


        # draw the center lines
        cv2.line(img=frame, pt1=(0, int(y_cam/2)), pt2= (x_cam, int(y_cam/2)), color=(0, 0, 255), thickness=1, lineType=8, shift=0)  # line in the x axis
        cv2.line(img=frame, pt1=(int(x_cam/2), 0), pt2=(int(x_cam/2), y_cam), color=(0, 0, 255), thickness=1, lineType=8, shift=0)  # line in the y axis

        # draw the active tracking area (boundries of the precision area)

        cv2.line(img=frame, pt1=(x1, y0), pt2=(x0, y0), color=(0, 0, 255), thickness=1, lineType=8, shift=0)  # line in the x axis
        cv2.line(img=frame, pt1=(x0, y0), pt2=(x0, y1), color=(0, 0, 255), thickness=1, lineType=8, shift=0)  # line in the x axis
        cv2.line(img=frame, pt1=(x0, y1), pt2=(x1, y1), color=(0, 0, 255), thickness=1, lineType=8, shift=0)  # line in the x axis
        cv2.line(img=frame, pt1=(x1, y1), pt2=(x1, y0), color=(0, 0, 255), thickness=1, lineType=8, shift=0)  # line in the x axis
        
    


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
                    wp, hp = int(lm.x * w), int(lm.y * h)  
                    current_lm = [hand_id, finger_id, wp, hp]  # gets the coordenates of the landmark in PIXELS

                    
                    if current_lm[1] == 8: # obs: the index finger tip is the landmark with the id = 8
        
                        
                        # OBS: If the value of the x coordinate is 0 it doens't apear on the variable xy because its on the left of the number 
                        xy = current_lm[2:]  # gets just the coordenates of the index finger tip
                        intervals = get_interval(xy)  # gets the intervals in the acreen of the finget tip
                        #print(xy)
                        #print(intervals)
                        
                        # A buffer was used because the previous version of the code sent values through serial only when the current position was different from the one before
                        del buffer_x[0] # removes the first element of the x list
                        buffer_x.append(intervals[0]) # adds the new value to the last x list position
                        del buffer_y[0] # removes the first element of the y list
                        buffer_y.append(intervals[1]) # adds the new value to the last y list position


                        # Controls the x movement
                        if (buffer_x[1]) >= ((sections - 1)/2 + x_prec_interval):  # if the object went left to the tracking area 
                            if (buffer_x[1] != buffer_x[0]): # if the object is moving -> ensures the values is gonna be sent only once so the controller buffer doenst get full
                            # Sends the coordinates to the serial port
                                serial_send('1')


                        elif (buffer_x[1]) <= ((sections - 1)/2 - x_prec_interval):  # if the object went right to the tracking area
                            if (buffer_x[1] != buffer_x[0]):
                            # Sends the coordinates to the serial port
                                serial_send('2')


                        # Controls the y movement
                        elif (buffer_y[1]) >= ((sections - 1)/2 + y_prec_interval):  # if the object went down to the tracking area
                            if (buffer_y[1] != buffer_y[0]):
                            # Sends the coordinates to the serial port
                                serial_send('3')


                        elif (buffer_y[1]) <= ((sections - 1)/2 - y_prec_interval):  # if the object went up to the tracking area
                            if (buffer_y[1] != buffer_y[0]):
                            # Sends the coordinates to the serial port
                                serial_send('4')


                        else:  # ensures the camera stops when the object gets recentered
                            if (buffer_x[1] != buffer_x[0]) or (buffer_y[1] != buffer_y[0]):
                            # Sends the coordinates to the serial port
                                serial_send('0')
                    




                                                    
                            

                        



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
    

    