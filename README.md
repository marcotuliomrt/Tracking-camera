# Tracking-camera
A camera that redirects itself to center predefined target object on the screen. The hand_tracker.py scripts tracks specifically the index finger tip.

## How it works 
The camera mounted on a base buil on 2 servo motors follows predefined objects. More specifically, a python script runs on the PC processing images from the camera, gets the coordinates of a desired point and send commands through UART to the microcontroller that controls the servo motors, which redirects the camera so the object being tracked stays on the center os the image.
### - Image processing
The purpose of the image processing is to get the coordinates of the desired point in real time, but for this is necessary to make object detection first. Then, the coordinates enter a function that generate 5 types of values, one tells the microcontroller to move the camera up, the other value to move it down,... left, right, and stop the camera where it is.
### - Object detetion
This project uses the OpenCV library, more specifically thir implementation of YOLOv4 for the multiple-onject detection and the Cascade
### - Hardware
The hardware is the simplest possible, l
### - What can be personalized 
On the hand_tracker.py, which tracks the index finger tip, its possible to change:
- The camera that is gonna be used: CAM_INDEX
- The number of section the ima is gonna be devided
- The precision of the tracking 

## Usage

To build the projets it's necessary both hardware and software correctly set.
Hardware:

## Materials used

