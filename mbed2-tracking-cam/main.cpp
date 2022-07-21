
//************************************************************************
//* 20-07-2022
//* Tracking-camera Marco_Tulio_Masselli
//************************************************************************

#include "mbed.h"

PwmOut servo_x(D5);
PwmOut servo_y(D6);
DigitalOut led1(D13);

Serial python(D8, D2, 9600);
Serial pc(USBTX, USBRX, 9600);

int MIN = 510;  //Min value the servos can reach
int MAX = 2350;  //Max value the servos can reach
int MID = (MAX + MIN)/2;  //Meddle value
int OFFSET = 300;  // How much the servos stop before reaching their limit (min and max values)

int STEP = 3;  // Steps the servo move every cycle of the loops
int CSTEP_x = MID; // current step of servo x
int CSTEP_y = MID; // current step of servo x
  
int state = 0;  // States represent their movement, if it's moving up, down, righ or left
char rx_line;

// Declaration of the funcitons
void Rx_interrupt();  
void calibrate();
void move_x(int dir, int max, int min, int step);
void move_y(int dir, int max, int min, int step);



int main() {
    
    // Everytime data comes through serial, the function Rx_interrupt is called
    python.attach(&Rx_interrupt, Serial::RxIrq);
    
    servo_x.period_us(20000); //20ms is the working period of the servos used
    servo_y.period_us(20000);
 
    calibrate();  // Calibration function call
 
    while(1){

        if(state == 1){
            pc.printf("state = 1\n");
            wait(0.1);
            while(state == 1){
                if(CSTEP_x < (MAX-OFFSET)){
                    servo_x.pulsewidth_us(CSTEP_x + STEP);
                    CSTEP_x = CSTEP_x + STEP;
                    wait(0.01);
                    }
                }
        }
        if(state == 2){
            pc.printf("state = 2\n");
            wait(0.1);
            while(state == 2){
                if(CSTEP_x > (MIN+OFFSET)){
                    servo_x.pulsewidth_us(CSTEP_x - STEP);
                    CSTEP_x = CSTEP_x - STEP;
                    wait(0.01);
                    }
                }
        }
        if(state == 3){
            pc.printf("state = 3\n");
            wait(0.1);
            while(state == 3){
                if(CSTEP_y < (MAX-OFFSET)){
                servo_y.pulsewidth_us(CSTEP_y + STEP);
                CSTEP_y = CSTEP_y + STEP;
                wait(0.01);
                }
            }
        }
        if(state == 4){
            pc.printf("state = 4\n");
            wait(0.1);
            while(state == 4){
                if(CSTEP_y > (MIN+OFFSET)){
                    servo_y.pulsewidth_us(CSTEP_y - STEP);
                    CSTEP_y = CSTEP_y - STEP;
                    wait(0.01);
                    }
                }
        }
        if(state == 5){
            wait(1);
        }
        
    }
    

}




    
    
    
void calibrate(){
    
    servo_x.pulsewidth_us(MID);
    wait(0.5);
    servo_y.pulsewidth_us(MID);
    wait(0.5);
    
    servo_x.pulsewidth_us(MID + 460);
    wait(0.5);
    servo_x.pulsewidth_us(MID - 460);
    wait(0.5);
    servo_x.pulsewidth_us(MID);
    
    
    wait(0.5);
    servo_y.pulsewidth_us(MID + 460);
    wait(0.5);
    servo_y.pulsewidth_us(MID - 460);
    wait(0.5);
    servo_y.pulsewidth_us(MID);
    
    wait(0.5);
    
    
    
    }




void Rx_interrupt() // function that receives the outputs from the python script
{

    while(python.readable())
    

    // rx_line receives hte value of the char from the buffer of the "python" device
    rx_line = python.getc();
    
    switch(rx_line) 
    {

        case '1':
            state = 1;
            rx_line = 0x00;
            break;

        case '2':
            state = 2;
            rx_line = 0x00;
            break;
            
        case '3':
            state = 3;
            rx_line = 0x00;
            break;
            
        case '4':
            state = 4;
            rx_line = 0x00;
            break;
            
        case '5':
            state = 5;
            rx_line = 0x00;
            break;
            
            
            
            default: rx_line=0;

    }
    return;
}
