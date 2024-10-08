import datetime
import pytz
import time
import support
MAX_TEMP = 23.4
MIN_TEMP = 19


time_interval = 55
current_temp = 23.3


# Decreses the temperature by 0.1 degree Celsius every time_interval 
# untill the temperature reaches MAX_TEMP
def temperature_down():
    print(f"Decreasing the temp at {datetime.datetime.now()}")
    global current_temp

    while round(current_temp, 1) != MIN_TEMP:
        support.set_temp(current_temp)

        time.sleep(time_interval)
        current_temp -= 0.1

   
# Increases the temperature by 0.1 degree Celsius every time_interval 
# untill the temperature reaches MAX_TEMP
def temperature_up():
    print(f"Increasing the temp at {datetime.datetime.now()}")
    global current_temp


    while round(current_temp, 1) != MAX_TEMP:
        support.set_temp(current_temp)

        current_temp += 0.1

        time.sleep(time_interval)

# Maintains a relatively steady temperature for 6 * tinme_interval
def temperature_flat():
    print(f"Keeping the temperature flat at {datetime.datetime.now()}")

    global current_temp

    count = 0

    while count != 6:
        #support.set_temp(current_temp)

        if (count % 2) == 0:
            current_temp += 0.1
        else:
            current_temp -= 0.1

        time.sleep(time_interval)   
        count += 1



def main():
    global time_interval

    time_zone = pytz.timezone("America/New_York")

    # End the program July 15th at 8:30 AM
    end_time = datetime.datetime(2024, 7, 16, 8, 30, 20)
    end_time = time_zone.localize(end_time)

    print(f"Week end testing started at {datetime.datetime.now()} ...")
    
    while True:
        #we want the temperature to make a sin curve around the set point of 21.1

        temperature_down()

        temperature_up()

        time.sleep(1)
    
    print(f"The program finished at {datetime.datetime.now()}")

if __name__ == "__main__":
    main()