# Tracking-camera
A camera that redirects itself to center predefined target object on the screen. Each script whose name end with "_tracker.py" track one object, for example the hand_tracker.py script tracks only the index finger tip.

## How it works 
The camera mounted on a base buil on 2 servo motors follows predefined objects. More specifically, a python script runs on the PC processing images from the USB camera, gets the coordinates of a desired point and send some commands through UART to the microcontroller that controls the servo motors, which redirects the camera so the object being tracked stays on the center os the image.

### - Image processing
The purpose of the image processing is to get the coordinates of the desired point in real time, but for this is necessary to make object detection first. Then, the coordinates enter a function that generate the commands to move the servo motors. There are 5 commands, one tells the microcontroller to move the camera up, the other value to move it down,... left, right, and stop the camera where it is.

### - Camera movement / servo commands
The logic of the traslation of coordinates into servo movement commands is based on a screen segmentation, what could be interpreted as the resolution of the tracker, the smallest space unit that the camera can track. For example, if the screen is devide on a big number of segments (what means each unit is small) means that even a slight movement of the object would translate into a movement of the camera

### - Object detetion
This project uses the OpenCV library, more specifically their implementation of YOLOv4 for the multiple-object detection and the HaarCascade weiths for the neural network.

### - Hardware
The hardware is the simplest possible, just enough to allow 2 degrees of freedom to the camera. It is composed by: 
- 1 STM32 F401RE Microcontroller on the nucleo development board
- 1 Power supply (used on 5V for the servo motors)
- 2 HXT900 servo motors
- 1 old laptop camera. 

### - What can be personalized 
These variables are on the beginning og hte code and information about its values is availuable on comments on the code.
On the every "_tracker.py" script:
- The camera that is gonna be used: CAM_INDEX
- The number of section the image is gonna be devided: SECTIONS
- The precision of the tracking: X_PRECISION, Y_PRECISION
- The serial port for the UART communication: PORT 

## Usage
To build the projets it's necessary both hardware and software correctly set.
Hardware:
