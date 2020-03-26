// IBT2 Library Example
//
// Ramps the IBT-2 output up from 0 to 100% forward, down to 100% reverse,
// and then back to 0 and repeats.
//
// The target is the FRDM-K64F board. You can hook up the EN lines directly to
// Vcc if you want to, but I have included them here for completeness.
//
// IBT-2 connections:
//   L_PWM -> PTC10 = Pin A1
//   R_PWM -> PTC11 = Pin A2
//   L_EN  -> PTB11 = Pin A3
//   R_EN  -> PTB10 (or just wire to PTB11) = Pin A4
//   L_IS  -> not used
//   R_IS  -> not used
//   VCC   -> 3.3V
//   GND   -> GND
//   B+    -> Power + (6-28V)
//   B-    -> Power -
//   M+    -> Load +
//   M-    -> Load -
 
#include "mbed.h"
#include <string>
#include "IBT2.h"


//PwmOut L_PWM(A1);
//PwmOut R_PWM(A2);
DigitalOut en(A3);
I2CSlave slave(D4,D5);
//DigitalOut R_en(A4);    // only because I used 2 wires
DigitalIn motor_enable(D3);
IBT2 ibt(A1, A2, A3, 10000.0);    // L_pwm, R_pwm, en, freq

//// manually enable the second enable line (R_EN)


//
//
void motor(string direction)
{
    // setup
    float speed = 0.0;
    float ds = 0.5;    // start ramping up
    float max_speed = 0.5; // set max speed
//    R_en = 1;    // manually enable the R_EN line
    
    // loop
    while (true) {
        
         if (motor_enable == 0){
            printf("Please enable motor from ESP32!\n");
            speed = 0;
            break;
        }    
        
        printf("Motor is running .... \n");
        
        if (direction == "F"){
            printf("Forward\n");
            ibt.setSpeed(speed);
        }
        
        else if (direction == "L" or direction == "R"){
            printf("Turn left or right!");
            ibt.turnDirection(direction,speed);
        }
        
        else if (direction == "B"){
            ibt.setSpeed(0);
            break;
        }
        
        else{
            break;
        }
        
        if (speed >= max_speed){
            printf("Speed reach max_speed\n");
            break;
        }
        
        // set up the next speed
        speed += ds;
       // if (speed > 1.0f) {
//            speed = 1.0;
//            ds = -ds;    // stop at 1.0 and begin to ramp down
//        }
        
        printf("Speed : %lf\n",speed);
        
        
        
        wait(0.5);
        
    }
}


int main() {
    
    char buf[20];
    printf("STM32 started...\n");
    slave.address(0xA0); // actual address = 0x50 (last bit ignored)
    while (1) {
        for(int i = 0; i < sizeof(buf); i++) buf[i] = 0; // Clear buffer          
        int i = slave.receive();
        switch (i) {
            case I2CSlave::ReadAddressed:
                continue;
            case I2CSlave::WriteAddressed:
                slave.read(buf,sizeof(buf)-1);
                printf("Read: %s\n", buf);
                motor(buf);
                continue;
        }
    }

}