from machine import Pin
import time
import network
import urequests

class stationClass():
    
    def __init__(self , led_pin , coming_pin , arrived_pin , station_num):
        
        led = Pin(led_pin, Pin.OUT) # On board LED
        led.value(0) # init value of LED
        
        coming = Pin(coming_pin, Pin.OUT)
        coming.value(0)
        arrived = Pin(arrived_pin, Pin.OUT)
        arrived.value(0)
        
        
        self.led = led
        self.coming = coming
        self.arrived = arrived
        self.station_num = station_num
    
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
        
    
    def get_status(self):
        
        url = "http://192.168.1.12:5000/station?station="+str(self.station_num)
        
#         print("GET data at : ",url)
        
        response = urequests.get(url)
        
        data = response.text
        
        return data
    
    
    def update_status(self):
        
        try:
            
            time.sleep(0.5)
        
            data = self.get_status()
            
        except Exception as e:
            
            print(e)
            time.sleep(0.5)
            
            return 0
        
        print("data : ",data)
        
        if data == "coming":
            
            self.coming.value(1)
            self.arrived.value(0)
        
        elif data == "arrived":
            
            self.arrived.value(1)
            self.coming.value(0)
            
        elif data == "avaliable":
            
            self.arrived.value(0)
            self.coming.value(0)
    

    def hotspot_sharing(self):

        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid="Station"+str(self.station_num)+"_AP")
        
        
        
if __name__ == "__main__":
    
    station = stationClass(led_pin=2,coming_pin=16,arrived_pin=17,station_num=3)
    
    station.connect_to_wlan("YakNonBangKwang","123456789")
    
    station.hotspot_sharing()
    
    while True:
        
        station.update_status()
        time.sleep(0.1)
        