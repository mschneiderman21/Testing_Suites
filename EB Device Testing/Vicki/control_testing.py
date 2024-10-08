import vicki_ttsApi
import time
import datetime
import random
import math

TARGET_TEMP = 21.1

max_temp = 25.1
min_temp = 17.1
current_temp = 25.1
time_interval = 1


def target_temp(temp):
    temp = hex(int(temp * 10))[2:]
    while len(temp) < 4: temp = "0" + temp

    payload = "51" + temp[:2] + temp[2:] 
    frm_payload = vicki_ttsApi.toBase64(payload)
    vicki_ttsApi.downlink(frm_payload)

def set_temp(temp):
    temp = hex(int(temp * 10))[2:]
   
    while len(temp) < 4: temp = "0" + temp

    payload = "3c" + temp[:2] + temp[2:] 
    frm_payload = vicki_ttsApi.toBase64(payload)
    vicki_ttsApi.downlink(frm_payload)

def temperature_up():
    print(f"Increasing the temp at {datetime.datetime.now()}")
    global current_temp, min_temp

    while round(current_temp, 1) != max_temp:
        set_temp(current_temp)

        current_temp += 0.1

        time.sleep(time_interval)

        if current_temp == 21.1:
            min_temp = min_temp + 0.2

# Decreses the temperature by 0.1 degree Celsius every time_interval 
# untill the temperature reaches MIN_TEMP
def temperature_down():
    print(f"Decreasing the temp at {datetime.datetime.now()}")
    global current_temp, max_temp

    while round(current_temp, 1) != min_temp:
        set_temp(current_temp)

        time.sleep(time_interval)
        current_temp -= 0.1

        if current_temp == 21.1:
            max_temp = max_temp - 0.2

def temperature_flat():
    print(f"Keeping the temperature flat at {datetime.datetime.now()}")

    global current_temp

    count = 0

    while count != 4:
        #support.set_temp(current_temp)

        if (count % 2) == 0:
            current_temp += 0.1
        else:
            current_temp -= 0.1
        set_temp(current_temp)

        time.sleep(time_interval)   
        count += 1

def log_up():
    global current_temp
    start_temp = current_temp
    ln = 1.1
    count = 0
    while (TARGET_TEMP - current_temp > 0):
        current_temp = round(start_temp + math.log(ln), 1)
        ln = ln + 0.1
        count =  count + 1
        print(f"{count}, {current_temp}")

def log_down():
    global current_temp
    start_temp = current_temp
    ln = 1.1
    count = 0
    while (current_temp - TARGET_TEMP > 0):
        current_temp = round(start_temp - math.log(ln), 1)
        ln = ln + 0.1
        count =  count + 1
        print(f"{count}, {current_temp}")
        

def random_temperature():
    global min_temp, max_temp, current_temp
    count = 0
    print("Time,Temperature")
    while (max_temp - min_temp) > 0.1:
        add_sub = 0
        if random.random() < 0.5:
            add_sub = 1 
        else:
            add_sub = -1
        
        current_temp = round(current_temp + (random.randint(1,3) * 0.1 * add_sub), 1)

        print(f"{count},{current_temp}")
        
        count = count + 1

        if (count % 1000 == 0):
            time.sleep(time_interval)

        if (current_temp - min_temp) < 0:
            current_temp = current_temp + 0.4
        elif (max_temp - current_temp) < 0:
            current_temp = current_temp - 0.4
        
        # print(f"MIN: {min_temp} and MAX: {max_temp}")


def main():
    # frm_payload = vicki_ttsApi.toBase64("0701")
    # vicki_ttsApi.downlink(frm_payload)

    # time.sleep(time_interval)

    # target_temp(TARGET_TEMP)
    #print(f"The program began running at {datetime.datetime.now()} ")
    # time.sleep(time_interval)

    log_down()
    #time.sleep(100)
    
    print(f"The program finished running at {datetime.datetime.now()} ")
    #time.sleep(55)
    #frm_payload = vicki_ttsApi.toBase64("0700")

if __name__ == "__main__":
    main()