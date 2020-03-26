from hcsr04 import HCSR04
from machine import Pin , I2C
import network
import time
import _thread
import urequests

class carClass():
    
    def __init__(self, led_pin, motor_pin , HCSR1_pin_trig, HCSR1_pin_echo, HCSR2_pin_trig, HCSR2_pin_echo):
        
        led = Pin(led_pin, Pin.OUT) # On board LED
        led.value(0) # init value of LED
        motor = Pin(motor_pin, Pin.OUT) # Send message to NucleoL432KC
        sensor1 = HCSR04(trigger_pin=HCSR1_pin_trig, echo_pin=HCSR1_pin_echo) # Distance sensor
        sensor2 = HCSR04(trigger_pin=HCSR2_pin_trig, echo_pin=HCSR2_pin_echo) # Distance sensor
        i2c = I2C(scl=Pin(22),sda=Pin(21),freq=100000)
        
        
        self.i2c = i2c
        self.busy = 0
        self.led = led
        self.motor = motor
        self.sensor1 = sensor1
        self.sensor2 = sensor2
        self.stop_avoidance = 0
        self.motor_stop_by = -1
        self.velocity = 0.3 # m/s
        self.break_time = 0 # s
        self.turn_l_time = 3.5 # s
        self.turn_r_time = 3.5 # s
        self.stop_time = 5 # s
        self.reverse = 0

        
    def scan(self):
        
        wlan = self.wlan

        scan_list = wlan.scan()
        
        rssi = {}

        print("scan complete : ",scan_list)
        
        wifi_num = 0

        for i in scan_list:
            wifi_name = str(i[0])[2:len(str(i[0]))-1]
            channel = i[2]
            RSSI = i[3]
            if wifi_name == "Station1_AP":
                
                rssi.setdefault(wifi_name,RSSI)
                wifi_num += 1
                
            elif wifi_name == "Station2_AP":
                
                rssi.setdefault(wifi_name,RSSI)
                wifi_num += 1
                
            elif wifi_name == "Station3_AP":
                
                rssi.setdefault(wifi_name,RSSI)
                wifi_num += 1
                
        if ("Station1_AP" in rssi) and ("Station2_AP" in rssi) :
            print(rssi)
            return rssi
        else:
                return -1
                
            # print("Wifi name :",wifi_name,", Channel :",channel,", RSSI :",RSSI)
        
        
    def check_distance(self,sensor,motor , number):
        
        while True:
        
            if self.stop_avoidance == 1:
                
                return 1
                
            sum = 0
            
            i = 0
            
            while i < 3:

                distance = sensor.distance_cm()
                
                if distance <= 0.1:
                    ## print("Less than 0.1 : i = ",i)
                    
                    i-=1
                    if i <= -4:
                        if i <= -7:
                            self.breakk()
                            continue
                        self.forward()
                    continue
                    
                else:
                    if i < 0:
                        i = 0
                    sum += distance
                    
                i+=1
                
            distance = distance / 3
            
            print("Number : ",number ,"Distance : ",distance,"m.")
            
            if distance <= 30:
                
                self.breakk()
                self.motor_stop_by = number
            
            elif distance >= 35:
                
                if self.motor_stop_by == number or self.motor_stop_by == -1:
                
                    self.forward()
                    self.motor_stop_by = 0
                
    def check_break_time(self):
        
        motor = self.motor
        
        while motor.value() == 0:
            self.break_time += 1
            time.sleep(1)
        
        
    def get_direction(self , rssi1 , rssi2):
        
        url = "http://192.168.1.12:5000/mapping?rssi1="+str(rssi1)+"&rssi2="+str(rssi2)
        
        response = urequests.get(url)
        
        print("Getting at",url)
        
        data = response.text
        
        return data
    
    def finish(self):
        
        url = "http://192.168.1.12:5000/finish"
        response = urequests.get(url)
        
        self.busy = 0
    
    
    def get_mapping(self):
        
        try:
        
            self.busy = 1
            
            distance = self.scan()
            if distance == -1:
                return 1
            
            rssi1 = distance["Station1_AP"]
            rssi2 = distance["Station2_AP"]
#             rssi3 = distance["Station3_AP"]
            
            direction = self.get_direction(rssi1,rssi2)
#             direction = self.get_direction(-40,-50,-60)
            
            if direction == "-1":
                return 1
            else:
                direction = direction.split(',')
                print(direction)
                return direction
        
        except Exception:
            
            print("Error!!")
            
            return 1
        
    def forward(self):
        self.motor.value(1)
        print("F")
        success = 0
        while (success == 0):
            try:
                self.i2c.writeto(0x50, b'F')
                success = 1
            except Exception as e:
                print("Error!! :",e)
                continue
        
    def right(self):
        self.motor.value(1)
        print("R")
        success = 0
        while (success == 0):
            try:
                self.i2c.writeto(0x50, b'R')
                success = 1
            except Exception as e:
                print("Error!! :",e)
                continue
        
    def left(self):
        self.motor.value(1)
        print("L")
        success = 0
        while (success == 0):
            try:
                self.i2c.writeto(0x50, b'L')
                success = 1
            except Exception as e:
                print("Error!! :",e)
                continue
        
    def breakk(self):
        self.motor.value(1)
        print("B")
        success = 0
        while (success == 0):
            try:
                self.i2c.writeto(0x50, b'B')
                success = 1
            except Exception as e:
                print("Error!! :",e)
                continue
        
    def working(self):
        
#         print("Check Work")
        mapp = self.get_mapping()
        if mapp == 1:
#             print("Return working")
            return 1
#         print("Working")
        time_to_start_station = float(mapp[1])/self.velocity
        start_direction = mapp[0]
        time_to_destination_station = float(mapp[3])/self.velocity
        destination_direction = mapp[2]
        
        self.forward()
        time.sleep(time_to_start_station)
        while self.break_time != 0:
            time.sleep(self.break_time)
            self.break_time = 0
        self.breakk()
        time.sleep(0.2)
        self.stop_avoidance = 0
        if start_direction == "L":
            self.left()
            time.sleep(self.turn_l_time)
            self.breakk()
            time.sleep(0.1)
            self.forward()
            time.sleep(0.1)
            self.breakk()
            time.sleep(self.stop_time) ###### for carry something
            if time_to_start_station >= time_to_destination_station:
                self.reverse = 1
                self.left()
                time.sleep(self.turn_l_time)
                self.breakk()
            else:
                self.right()
                time.sleep(self.turn_r_time)
                self.breakk()
            
        elif start_direction == "R":
            self.right()
            time.sleep(self.turn_r_time)
            self.breakk()
            time.sleep(0.1)
#             self.forward()
            time.sleep(0.1)
            self.breakk()
            time.sleep(5) ###### for carry something
            if time_to_start_station >= time_to_destination_station:
                self.reverse = 1
                self.right()
                time.sleep(self.turn_r_time)
                self.breakk()
            else:
                self.left()
                time.sleep(self.turn_l_time)
                self.breakk()
        
        self.stop_avoidance = 1
        
        mapp = self.get_mapping()
        if mapp == 1:
            return 1
        time_to_start_station = float(mapp[1])/self.velocity
        start_direction = mapp[0]
        time_to_destination_station = float(mapp[3])/self.velocity
        destination_direction = mapp[2]
        
        self.forward()
        time.sleep(time_to_destination_station)
        while self.break_time != 0:
            time.sleep(self.break_time)
            self.break_time = 0
        self.breakk()
        time.sleep(0.2)
        self.stop_avoidance = 0
        if destination_direction == "L":
            
            if self.reverse == 0:
                self.left()
                time.sleep(self.turn_l_time)
                self.breakk()
                time.sleep(0.1)
                self.forward()
                time.sleep(0.1)
                self.breakk()
                time.sleep(0.1)
                self.left()
                time.sleep(self.turn_l_time)
                self.breakk()
                
            else:
                self.reverse = 0
                self.right()
                time.sleep(self.turn_r_time)
                self.breakk()
                time.sleep(0.1)
                self.forward()
                time.sleep(0.1)
                self.breakk()
                time.sleep(0.1)
                self.right()
                time.sleep(self.turn_r_time)
                self.breakk()
            
        elif destination_direction == "R":
            if self.reverse == 0:
                self.right()
                time.sleep(self.turn_r_time)
                self.breakk()
                time.sleep(0.1)
#                 self.forward()
                time.sleep(0.1)
                self.breakk()
                time.sleep(0.1)
                self.right()
                time.sleep(self.turn_r_time)
                self.breakk()
            else:
                self.reverse = 0
                self.left()
                time.sleep(self.turn_l_time)
                self.breakk()
                time.sleep(0.1)
                self.forward()
                time.sleep(0.1)
                self.breakk()
                time.sleep(0.1)
                self.left()
                time.sleep(self.turn_l_time)
                self.breakk()
        
        self.stop_avoidance = 1
            
        print("End")
        
        self.finish()
        time.sleep(3)
        self.finish()
        time.sleep(1)
        
        
        
                    
    def connect_to_wlan(self, name , password):
        
        led = self.led

        wlan = network.WLAN(network.STA_IF) # create station interface
        wlan.active(True)       # activate the interface

        wlan.disconnect()

        while wlan.isconnected():
            
            time.sleep(1)


        wlan.connect(name,password) #connect wireless

        a = 0

        while not wlan.isconnected():

            # print(wlan.status)

            # print(wlan.isconnected())
            
            led.value(a%2) # Blink Waiting for connection
            
            a+=1
            
            time.sleep(1)
            
        led.value(1) # LED ON when connect to network successfully
        
        time.sleep(1)
        
        self.wlan = wlan
        
        
    def hotspot_sharing(self,name):

        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=name)
        
    def stop(self):
        
        self.stop_avoidance = 1
        self.led.value(0)
        self.wlan.disconnect()
        self.breakk()
        
        
    
if __name__ == "__main__":
    
#     print("--------------------  init  ------------------")
    
    mycar = carClass(led_pin=2,motor_pin=5,HCSR1_pin_trig=16,HCSR1_pin_echo=0,HCSR2_pin_trig=17,HCSR2_pin_echo=4)

    wlan = mycar.connect_to_wlan("YakNonBangKwang","123456789") # connect to WLAN
    
    
    time.sleep(3)
     
#     _thread.start_new_thread(mycar.check_distance,(mycar.sensor1,mycar.motor ,1)) # start new thread for object avoidance
#     _thread.start_new_thread(mycar.check_distance,(mycar.sensor2,mycar.motor ,2)) # start new thread for object avoidance
    
#     j = 0
    
    while True:
        
        mycar.working()
        
        time.sleep(0.5)
#         j+=1
        
    mycar.stop()
    
  
        






     










        