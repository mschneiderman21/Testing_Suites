import datetime
import tts_downlinks
import time
import pytz
import json
#import js2py

time_zone = pytz.timezone("America/New_York")

def main():
    keep_sending_temp()

def wait_until():
    now = datetime.datetime.now(time_zone)
    next = (now + datetime.timedelta(days=0)).replace(hour=20, minute=0, second=0, microsecond=0)
    time_till_start = (next - now).total_seconds()
    print(f"Waiting for {time_till_start} seconds until start.")
    time.sleep(time_till_start + 120)
    print("It's Time! Starting the program...") 

def check_control_status():
    uplink = tts_downlinks.get_uplinks(1)
    
    json_string = uplink.decode('utf-8')
    data = json.loads(json_string)
    print(data)

    frm_payload = data['result']['uplink_message']['decoded_payload']['temperature_control_status']

    print(frm_payload)
    
    # hex = tts_downlinks.toHex(frm_payload)
    
    if ("test" == "standby"):
        return False
    else:
        return True

def keep_sending_temp():
    # temp = hex(int(float(temp) * 10) )[2:]
    # while len(temp) < 4:
    #     temp = "0" + temp

    # payload = "03" + temp[2:] + temp[:2] + "00"

    #print(f"Sending {temp} every {frequency/60} minutes")

    reset = [("03d60000", 50)]
    while True:
        for tuple in reset:
            time.sleep(tuple[1])
            frm_payload = tts_downlinks.toBase64(tuple[0])
            tts_downlinks.downlink(frm_payload)
            #print(f"Sent temp at: {datetime.datetime.now()}")

            #check_control_status()

def c_to_f():
    temp = input("Enter your desired temp: ")
    f_temp = round((float(temp) * 9/5) + 32, 2)
    print(f_temp)

def f_to_c():
    temp = input("Enter your desired temp: ")
    f_temp = round((float(temp) - 32 ) * 5/9, 2)
    print(f_temp)

def set_temp(temp):
    temp = hex(int(temp * 10))[2:]
   
    while len(temp) < 4: temp = "0" + temp

    payload = "03" + temp[2:] + temp[:2] + "00"
    frm_payload = tts_downlinks.toBase64(payload)
    tts_downlinks.downlink(frm_payload)

if __name__ == "__main__":
    main()