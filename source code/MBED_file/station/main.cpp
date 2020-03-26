#include "mbed.h"
#include "Servo.h"
#include "Adafruit_SSD1306.h"

#define SDA D4
#define SCL D5
#define ARRIVED 2
#define COMING 1
#define AVAILABLE 0
//// Config INPUT HERE /////////
DigitalIn Avaliable(D9,PullDown);   
DigitalIn Coming(D10,PullDown);   
DigitalIn Arrived(D11,PullDown);   
///////////////////////////////
I2C i2c(SDA, SCL);
DigitalOut led1(D6);
Servo servo(A1); 

Adafruit_SSD1306_I2c oled(i2c,D9);
int status = -1;


void update_state(){
    
//    if (Coming == 1 && Avaliable == 0 && Arrived == 0){
//        status = COMING;
//    }
//    else if (Coming == 0 && Avaliable == 1 && Arrived == 0){
//        status = AVAILABLE;
//    }
//    else if (Coming == 0 && Avaliable == 0 && Arrived == 1){
//        status = ARRIVED;
//    }
//    else{
//        status = -1;
//    }
    
    if (Arrived == 1){
        printf("Arrived\n");
        status = ARRIVED;
    }
    
    else if (Coming == 1){
        printf("Coming\n");
        status = COMING;
    }
    
    else if (Avaliable == 1){
        printf("Avaliable\n");
        status = AVAILABLE;
    }
     
     
    else{
        status = -1;
    }
    wait(0.1);
}

int main()
{
    
    oled.clearDisplay();
    servo = 1 ;   
    while(1) {
        
        update_state();
        
        if (status == -1){
            continue;
        }
        
        printf("%d",status);

        oled.clearDisplay();

        if (status == AVAILABLE) {
            servo = 1;
            led1 = 0;
            oled.setTextCursor(0,0);
            oled.printf("S3");
            oled.setTextCursor(45,14);
            oled.printf("AVAILABLE");
            status = -1;
        }
        
        else if (status == COMING) {
            servo = 1;
            led1 = 1;
            oled.setTextCursor(0,0);
            oled.printf("S3");
            oled.setTextCursor(50,14);
            oled.printf("COMING");   
            status = -1; 
        }
        
        else if (status == ARRIVED) {
            servo = 0;
            led1 = 1;
            oled.setTextCursor(0,0);
            oled.printf("S3");
            oled.setTextCursor(47,14);
            oled.printf("ARRIVED");
            status = -1;
        }
        
        oled.display();
        wait(0.1); 
    }
}