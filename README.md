# Tracking-camera
A camera that redirects itself to center predefined target object on the screen. Each script whose name end with "_tracker.py" track one object, for example the hand_tracker.py script tracks only the index finger tip.

## How it works 
The camera mounted on a base buil on 2 servo motors follows predefined objects. More specifically, a python script runs on the PC processing images from the USB camera, gets the coordinates of a desired point and send some commands through UART to the microcontroller that controls the servo motors, which redirects the camera so the object being tracked stays on the center os the image.
### - Image processing
The purpose of the image processing is to get the coordinates of the desired point in real time, but for this is necessary to make object detection first. Then, the coordinates enter a function that generate the commands to move the servo motors. There are 5 commands, one tells the microcontroller to move the camera up, the other value to move it down,... left, right, and stop the camera where it is.
### - Object detetion
This project uses the OpenCV library, more specifically their implementation of YOLOv4 for the multiple-object detection and the HaarCascade weiths for the neural network.
### - Hardware
The hardware is the simplest possible, just enough to allow 2 degrees of freedom to the camera. It is composed by: 
- 1 STM32 F401RE Microcontroller on the nucleo development board
- 1 Power supply (used on 5V for the servo motors)
- 2 HXT900 servo motors
- 1 old laptop camera. 

### - What can be personalized 
On the hand_tracker.py, which tracks the index finger tip, its possible to change:
- The camera that is gonna be used: CAM_INDEX
- The number of section the ima is gonna be devided
- The precision of the tracking 

## Usage

To build the projets it's necessary both hardware and software correctly set.
Hardware:

## Materials used

