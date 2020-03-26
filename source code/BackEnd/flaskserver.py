from flask import Flask, render_template, request, redirect, url_for

from pymongo import MongoClient

import math 



app = Flask(__name__)
client = MongoClient('localhost',27017)
mydatabase = client['SADC']
mycollection = mydatabase['Information']

###################### เปลี่ยนตัวแปร From เป็น src ###########################
###################### เปลี่ยนตัวแปร To เป็น dst ###########################

inf = {
    "Source":0,
    "SourceDirection":"",
    "Destination":0,
    "DestinationDirection":"",
    "Status":0,
    "Past_Src":0,
    "Past_Dst":0
}


def calculate_distance_rssi(number,rssi):

    txPower1 = -35 # Measure RSSI at 1 m from AP
    txPower2 = -35 # Measure RSSI at 1 m from AP
    txPower3 = -35 # Measure RSSI at 1 m from AP

    if number == 1:
        txPower = txPower1
    elif number == 2:
        txPower = txPower2
    elif number == 3:
        txPower = txPower3

    distance = math.pow(10, ((txPower - int(rssi)) / (10*2)))

    return distance





@app.route("/")
def Home():
    return render_template('index.html')

# ที่ route status จะเป็นตัวที่แสดงว่าเราทำงานถึงไหนแล้ว โดยให้บอร์ดส่งค่ามา มี 3 state ได้แก่
# ready = พร้อมใช้งาน
# working = ใช้งานไม่ได้ รถกำลังส่งของอยู่
# finish = รถถึงที่หมาย กลับมาถึงจุดเริ่มต้นแล้ว
# ** อาจจะบอก status เป็นตำแหน่งก็ได้เช่น สถานีไหนแล้ว จะแก้ไขส่วนนี้หลังจากรู้วิธีรับส่งข้อมูลกับบอร์ดแล้ว
# ตอนนี้แก้ขัดใช้แบบนี้ไปก่อน
@app.route("/Status")
def Status():
    findinf = mycollection.find_one()
    status = findinf["Status"]
    # status = 0 # ตามจริงต้องเป็นค่าที่รับมาจากรถ
    if status == 0:
        return render_template('Ready.html')
    elif status == 1:
        return render_template('Working.html')
    elif status == 2:
        status = 0
        return render_template('Finish.html')


@app.route("/insert",methods=['POST'])
def insert():
    src = int(request.form["Source"])
    srcDir = request.form["SourceDirection"]
    dst = int(request.form['Destination'])
    dstDir = request.form['DestinationDirection']
    inf["Source"] = src
    inf["SourceDirection"] = srcDir
    inf["Destination"] = dst
    inf["DestinationDirection"] = dstDir
    # inf["Status"] = 1
    if mycollection.count() == 0:
        rec = mycollection.insert_one(inf)
    else:
        findinf = mycollection.find_one()
        inf["Status"] = findinf["Status"]
        inf["Past_Src"] = findinf["Past_Src"]
        inf["Past_Dst"] = findinf["Past_Dst"]
        rec = mycollection.replace_one(findinf,inf) 
    return redirect(url_for('Status')) # status ควรเปลี่ยนเป็น working ทุกครั้งที่ refresh หน้า status จะไปตรวจสอบสถานะของรถแล้วนำมาแสดงผลหน้า status


@app.route("/mapping",methods=['GET'])
def mapping():

    try:

        # station1 = request.args.get('station1')
        rssi1 = request.args.get('rssi1')
        # station2 = request.args.get('station2')
        rssi2 = request.args.get('rssi2')
        # station3 = request.args.get('station3')
        rssi3 = request.args.get('rssi3')

        # global From
        # global To
        # global car_status
        # เปลี่ยนเป็น
        findinf = mycollection.find_one()
        src = findinf["Source"]
        dst = findinf["Destination"]
        car_status = findinf["Status"]
        

        car_status += 1

        
        # direction_from = "L"
        # direction_to = "R"
        # เปลี่ยนเป็น
        srcDir = findinf["SourceDirection"]
        dstDir = findinf["DestinationDirection"]


        if src == 1:
            start_distance = calculate_distance_rssi(src,rssi1)

        elif src == 2:
            start_distance = calculate_distance_rssi(src,rssi2)

        elif src == 3:
            start_distance =  calculate_distance_rssi(src,rssi3)

        else:
            start_distance = -1

        if dst == 1:
            destination_distance = calculate_distance_rssi(dst,rssi1)

        elif dst == 2:
            destination_distance = calculate_distance_rssi(dst,rssi2)

        elif dst == 3:
            destination_distance =  calculate_distance_rssi(dst,rssi3)

        else:
            destination_distance = -1


        if start_distance == -1 or destination_distance == -1:

            return "-1"

        return srcDir + ',' + str(start_distance) + ',' + dstDir + ',' +  str(destination_distance)

    except Exception:

        return "-1"

@app.route("/finish")
def finish():

    # global From
    # global To
    # global car_status
    # global past_From
    # global past_To
    findinf = mycollection.find_one()
    inf = findinf
    inf["Past_Src"] = findinf["Source"]
    inf["Past_Dst"] = findinf["Destination"]
    inf["Source"] = 0
    inf["SourceDirection"] = ""
    inf["Destination"] = 0
    inf["DestinationDirection"] = ""    
    inf["Status"] = 0
    mycollection.delete_many({})
    findinf = mycollection.find_one()
    rec = mycollection.insert_one(inf)

    # past_From = From
    # past_To = To
    # From = 0
    # To = 0
    # car_status = 0

    return "Success"


@app.route("/station")
def station():

    # global From
    # global To
    # global car_status
    # global past_To
    findinf = mycollection.find_one()
    src = findinf["Source"]
    dst = findinf["Destination"]
    car_status = findinf["Status"]
    Past_Dst = findinf["Past_Dst"]
    # print(car_status)

    station_num = int(request.args.get('station'))

    if car_status == 0 and station_num == Past_Dst:

        car_status = 1
        return "arrived"

    if station_num == src:

        if car_status == 2:

            return "coming"

        elif car_status == 3:

            return "arrived"

    elif station_num == dst:

        if car_status == 2 or car_status == 3:

            return "coming"

    else:

        return "avaliable"

    return "avaliable"



if __name__ == "__main__":
    app.run(debug=True , host="0.0.0.0")
    # app.run(debug=True)