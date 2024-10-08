from time import sleep
import tts_downlinks
# This returns the payload for basic settings
# COMMANDS IMPLEMENTED : Reboot, Querry Current Status
# Reporting Interval, System On/Off, Control Permission
# Child Lock, UTC Time Zone, Daylight Saving Time
# NOT IMPLEMENTED: Data Storage Data Retransmission, Data Retransmission Interval, Multicast Group

def basic():
    payload = ""
    print("\nWhat is your desired setting.")
    print("1. Reeboot")
    print("2. Querry Current Status")
    print("3. Reporting Interval")
    print("4. Temperature Control On/Off")
    print("5. Control Permission")
    print("6. Child Lock")
    print("7. UTC Time Zone")
    print("8. Daylight Saving Time")

    match input("\nEnter your selection: "):
        case "1":
            payload = "ff10ff"
        case "2":
            payload = "ff2801"
        case "3":
            payload = "ff8e00"
            interval = int(
                input("What is the desired interval (unit mins, i.e. 0001, max: 9999): "))
            # Convert the decimal value to hex and remove the "0x"
            payload += hex(interval)[2:]
            while len(payload) != 10:
                if len(payload) == 7:
                    temp = payload
                    payload = payload[:6] + "0" + temp[6:]
                payload += "0"
        case "4":
            power = input("0: Off  OR 1:On ")
            if power == "1" or power == "0":
                payload = "ffc50" + power   
            else:
                print("Not a valid input: Try again!")
        case "5":
            premission = input("0: Thermostat OR 1: Remote Control: ")
            if premission == "1" or premission == "0":
                payload = "fff60" + premission
            else:
                print("Not a valid input: Try again!")()
        case "6":
            print(
                "Child Lock Choices: System On/Off, Temp +, Temp -, Fan Mode, Temp Control, Reset/Reboot")
            print("For every bit enter either 0: Disable & 1: Enable:")
            # Convert binary string to hex string
            entry = hex(  # "11" can also be "00" does not affect reading of the payload
                int("11" + input("Should be 6 numbers (i.e. 100101): "), 2))[2:]
            payload = "ff25ff" + entry

            while len(payload) < 8:
                payload = payload[:6] + "0" + payload[6:]

        case "7":
            zone = int(input("What UTC time zone (i.e -4): ")) * 60
            if zone < 0:
                zone = hex2(zone)[2:]
                payload = "ffbd" + zone[2:] + zone[:2]
            elif zone > 0:
                zone = hex2(zone)[2:]
                if len(zone) == 2:
                    payload = "ffbd" + zone + "00"
                else:
                    payload = "ffbd" + zone[1:] + "0" + zone[:1]
            else:
                payload = "ffbd0000"
        case "8":
            payload = "ffba"

            enable = input("Input 0: Dsiable OR 1: Enable: ")
            if enable == "0":
                payload += "00"
            elif enable == "1":
                payload += "01"
            else:
                print("Not a valid input: Try again!")

            bias = hex(
                int(input("Input the amount of bias in minutes (Max: 255 mins): ")))[2:]
            payload += bias

            print("Now enter the start time.")
            for i in range(2):
                month = hex(
                    int(input("What month? Type 1 -> January, 2 -> Feburary, 3 -> March,... : ")))[2:]
                while len(month) < 2:
                    month = "0" + month

                week = input("What week? Type 1 -> 1st, 2 -> 2nd,... : ")
                while len(week) < 4:
                    week = "0" + week  # ensure week is 4 bits
                week = hex(int(week))[2:]

                day = input("What day? Type 1 -> Monday,..., 7 -> Sunday : ")
                while len(day) < 4:
                    day = "0" + day  # ensure day is 4 bits
                day = hex(int(day))[2:]

                time = hex(
                    int(input("What hour of the day? 0 - 24: ")) * 60)[2:]
                while len(time) < 4:
                    time = "0" + time  # ensure time is 4 bytes

                payload += month + week + day + time[2:] + time[:2]
            print("Now enter the end time.")
        case _:
            print("Invalid Input: Please try again!")
            basic()
    print("\nPayload is: " + payload)

    match input("Do you want to send the payload to the wt201? 0: No & 1: Yes "):
        case "1":
            send_payload(payload)


    match input("Return to main menu? 0: No & 1: Yes "):
        case "0":
            sleep(1)
            basic()
        case _:
            print("Returning to main menu...")
            sleep(1)

def hex2(n):
    return "0x%x" % (n & 0xffff)


def installation():
    print("Sorry, this has not been implemented yet. Returning to the main menu...")
    sleep(1)

# This returns the payload for thermostat control settings
# COMMANDS IMPLEMENTED : Temprature Control Mode, Target Temperature
# Temperature Tolerance, Fan Mode, Fan Delay
# Fan Circulate,
# NOT IMPLEMENTED: Fan Regulate Humidity, Target Humidity Range, Temp. Control and Dehumidify

def thermo_control():
    print("\nWhat is your desired setting.")
    print("1. Temprature Control")
    print("2. Temperature Tolerance")
    print("3. Fan Mode")
    print("4. Fan Delay")
    print("5. Fan Circulate")
    print("6. Fan Regulate Humidity")

    match input("\nEnter your selection: "):
        case "1":

            mode = "0" + \
                input("Enter the control mode (0: Heat, 1: EM Heat, 2: Cool, 3: Auto): ")

            unit = input("Enter 0 for Celsius and 1 for Farenheit: ")
            
            # Farenheit should be used for more precise temperatures as only whole numbers work. 
            temp = bin(int(input("Enter the target temp (must be a whole number): ")))[2:]

            if unit == "1": 
                temp = hex(int(temp, 2) | 0x80)[2:]
            else: temp = hex(int(temp, 2) & 0x7f)[2:]

            while len(temp) < 2: temp = "0" + temp
            payload = "ffb7" + mode + temp

        case "2":
            temp = hex(
                int(float(input("Enter the target tolerance (0 to 25.5 Celsius): ")) * 10))[2:]   
            
            while len(temp) < 2: temp = "0" + temp

            control = hex(
                int(float(input("Enter the control tolerance (0 to 25.5 Celsius): ")) * 10))[2:]

            while len(control) < 2: control = "0" + control    
            payload = "ffb8" + temp + control

        case "3":
            mode = "0" + \
                input("Enter the fan mode (0: Auto, 1: On, 2: Circulate, 3: Disable): ")
            payload = "ffb6" + mode
        case "4":
            enable = "0" + input("Input 0: Disable OR 1: Enable: ")
            delay = hex(
                int(input("Enter the amount of delay (5 - 55 mins):  ")))[2:]
            while len(delay) < 2:
                delay = "0" + delay

            payload = "f9055" + enable + delay

        case "5":
            time = hex(
                int(input("Enter the time for the fan to circulate (5 - 55 mins):  ")))[2:]
            while len(time) < 4:
                time = "0" + time
            payload = "f906" + time
        
        case "6":
            enable = input("Enter 00 - Disable and 01 - Enable: ")
            delay = hex(
                int(input("Enter the regulate interval (5 - 55 mins):  ")))[2:]
            
            while len(delay) < 2:
                delay = "0" + delay
            
            payload = "f907" + enable + delay

        case _:
            print("Invalid Input: Please try again!")
            thermo_control()
    print("\nPayload is: " + payload)

    match input("Do you want to send the payload to the wt201? 0: No & 1: Yes "):
        case "1":
            send_payload(payload)

    match input("Return to main menu? 0: No & 1: Yes "):
        case "0":
            sleep(1)
            thermo_control()
        case _:
            print("Returning to main menu...")
            sleep(1)


def remote_control():
    print("Sorry, this has not been implemented yet. Returning to the main menu...")

# This returns the payload for thermostat control settings
# COMMANDS IMPLEMENTED : Temprature Control Mode, Target Temperature
# Temperature Tolerance, Fan Mode, Fan Delay
# Fan Circulate,
# NOT IMPLEMENTED: Fan Regulate Humidity, Target Humidity Range, Temp. Control and Dehumidify

def calibration():
    payload = ""
    print("\nWhat is your desired setting.")
    print("1. Temperature Calibration")
    print("2. Humidity Calibration")
    print("3. Threshold Alarm")

    match input("\nEnter your selection: "):
        case "1":
            enable = "0" + input("Input 0: Disable OR 1: Enable: ")
            temp = hex2(
                int(float(input("Enter the calibration value (Celsius): ")) * 10))[2:]
            while len(temp) < 4:
                temp = "0" + temp

            payload = "ffab" + enable + temp[2:] + temp[:2]

        case "2":
            enable = "0" + input("Input 0: Disable OR 1: Enable: ")
            humidity = hex2(
                int(float(input("Enter the calibration value (%RH): ")) * 10))[2:]

            while len(humidity) < 4:
                humidity = "0" + humidity

            payload = "fff9" + enable + humidity[2:] + humidity[:2]

        case "3":
            payload = "ff06"
            print("\nWhat type of threshold alarm?")
            print("1. Temperature threshold")
            print("2. Presistent low temperature threshold")
            print("3. Presistent high temperatire threshold")

            match input("\nEnter your selection: "):
                case "1":
                    control = "0" + \
                        input(
                            "Input 0: Disable, 1: Below (minimum threshold), 2: Over (maximum threshold), 3: Within & 4: Below or Over: ")

                    low = hex(
                        int(float(input("Enter the min temperature (Celsius): ")) * 10))[2:]
                    while len(low) < 4:
                        low = "0" + low

                    high = hex(
                        int(float(input("Enter the max temperature (Celsius): ")) * 10))[2:]
                    while len(high) < 4:
                        high = "0" + high

                    payload += control + \
                        low[2:] + low[:2] + high[2:] + high[:2] + "00000000"
                case "2":
                    difference = hex(
                        int(input("Enter the difference value (Celsius): ")) * 10)[2:]
                    while len(difference) < 4:
                        difference = "0" + difference

                    time = hex(
                        int(input("Enter the duration (minutes): ")) * 60)[2:]
                    while len(time) < 4:
                        time = "0" + time

                    payload += "09" + \
                        difference[2:] + difference[:2] + \
                        "00000000" + time[2:] + time[:2]
                case "3":
                    difference = hex(
                        int(input("Enter the difference value (Celsius): ")) * 10)[2:]
                    while len(difference) < 4:
                        difference = "0" + difference

                    time = hex(
                        int(input("Enter the duration (minutes): ")) * 60)[2:]
                    while len(time) < 4:
                        time = "0" + time

                    payload += "120000" + \
                        difference[2:] + difference[:2] + \
                        "0000" + time[2:] + time[:2]
                case _:
                    print("Invalid Input: Please try again!")
                    calibration()
        case _:
            print("Invalid Input: Please try again!")
            calibration()

    print("\nPayload is: " + payload)

    match input("Do you want to send the payload to the wt201? 0: No & 1: Yes "):
        case "1":
            send_payload(payload)    

    match input("Return to main menu? 0: No & 1: Yes "):
        case "0":
            sleep(1)
            calibration()
        case _:
            print("Returning to main menu...")
            sleep(1)

# This returns the payload for schedule settings
# COMMANDS IMPLEMENTED : Schedule Content, Schedule Time, Switch Schedule Plan, Query Schedule

def schedule():
    print("\nWhat is your desired setting?")
    print("1. Schedule Content")
    print("2. Schedule Time")
    print("3. Switch Schedule Plan")
    print("4. Query Schedule")

    match input("\nEnter your selection: "):
        case "1":
            plan = "0" + \
                input("Enter the desired plan: 0-Wake, 1-Away, 2-Home & 3-Sleep ")
            fan = "0" + \
                input("Enter the desired fan mode: 0-Auto, 1-On & 2-Circulate ")

            unit = input(
                "Enter the desire target temperature unit: 0: C & 1: F ")
            target = bin(int(input("Enter the target temperature: ")))[2:]
            while len(target) < 7:
                target = "0" + target
            # add the unit
            target = hex(int(unit + target, 2))[2:]
            while len(target) < 2:
                target = "0" + target

            tolerance = hex(
                int(float(input("Enter the temperature tolerance: ")) * 10))[2:]
            while len(tolerance) < 2:
                tolerance = "0" + tolerance

            payload = "ffc8" + plan + "03" + fan + target + tolerance

        case "2":
            plan = "0" + \
                input("Enter the desired plan: 0-Wake, 1-Away, 2-Home & 3-Sleep ")
            identification = "0" + \
                hex(int(input("Enter the schedule time ID (0 - 15): ")))[2:]

            enable = "0" + input("Enable Repeat Day? 0: Disable & 1: Enable ")
            print("Repeat days Sunday to Monday: Enter 0 for Disable and 1 for Enable")
            repeat_days = hex(
                int(input("For each day enter enter a number (i.e 0111110): ") + "0", 2))[2:]
            
            while len(repeat_days) < 2: repeat_days = "0" + repeat_days

            time = hex(int(input(
                "Enter the desired start time of your plan (i.e 390 mins -> 6:30am or 810 mins -> 1:30pm): ")))[2:]
            while len(time) < 4:
                time = "0" + time

            payload = "ffc9" + plan + identification + \
                enable + repeat_days + time[2:] + time[:2]

        case "3":
            plan = "0" + \
                input("Enter the desired plan: 0-Wake, 1-Away, 2-Home & 3-Sleep ")
            payload = "ffc2" + plan

        case "4":
            payload = "ff2800"
        case _:
            print("Invalid Input: Please Try Again!")
            schedule()

    print("\nPayload is: " + payload)

    match input("Do you want to send the payload to the wt201? 0: No & 1: Yes "):
        case "1":
            send_payload(payload)

    match input("\nReturn to main menu? 0: No & 1: Yes "):
        case "0":
            sleep(1)
            schedule()
        case _:
            print("Returning to main menu...")
            sleep(1)



def milesight():
    print("Sorry, this has not been implemented yet. Returning to the main menu...")

# This returns the payload for external temperature settings
# COMMANDS IMPLEMENTED : External temperature sensor, send external temperature value 
def external():
    print("\nWhat is your desired setting?")
    print("1. External Temprature Sensor")
    print("2. Send External Temperature Value")

    match input("\nEnter your selection: "):
        case "1":
            enable = "0" + input("Input 0: Disable OR 1: Enable: ")

            time = hex(
                int(input("Enter the timeout time (mins up to 255): ")))[2:]
            while len(time) < 2:
                time = "0" + time

            payload = "ffc4" + enable + time
        case "2":
            temp = hex(
                int(float(input("Enter the external temperature value (Celsius): ")) * 10)) [2:]
            while len(temp) < 4:
                temp = "0" + temp

            payload = "03" + temp[2:] + temp[:2] + "00"

        case _:
            print("Invalid Input: Please try again!")
            external()

    print("\nPayload is: " + payload)

    match input("Do you want to send the payload to the wt201? 0: No & 1: Yes "):
        case "1":
            send_payload(payload)
    
    match input("Return to main menu? 0: No & 1: Yes "):
        case "0":
            sleep(1)
            external()
        case _:
            print("Returning to main menu...")
            sleep(1)


# This returns the payload for screen settings
# COMMANDS IMPLEMENTED : Screen enable/disable
def screen():
    enable = input(
        "\nDo you want to enable the screen display? 0: Enable, 1: Disable Plan Status, 2: Disable: ")
    payload = "f9080" + enable

    print("\nPayload is: " + payload)

    match input("Do you want to send the payload to the wt201? 0: No & 1: Yes "):
        case "1":
            send_payload(payload)

    match input("Return to main menu? 0: No & 1: Yes "):
        case "0":
            sleep(1)
            screen()
        case _:
            print("Returning to main menu...")
            sleep(1)



def history():
    print("Sorry, this has not been implemented yet. Returning to the main menu...")


def send_payload(payload):
    frm_payload = tts_downlinks.toBase64(payload)
    tts_downlinks.downlink(frm_payload)


def main():
    print("This program is used to get the payload messages for the wt201 smart thermostat.")
    while (True):
        print("\nWhat is your desired setting.")
        print("1. Basic Settings")
        print("2. Installation Settings")
        print("3. Thermostat Control Settings")
        print("4. Remote Control Settings")
        print("5. Calibration and Threshold Settings")
        print("6. Schedule Settings")
        print("7. Milesight D2D Settings")
        print("8. Use External Temperature Sensor")
        print("9. Screen Display Settings")
        print("10. Historical Data Enquiry")
        print("11. Exit Program")

        value = input("\nEnter your selection: ")
        sleep(1)

        match value:
            case "1":
                basic()
            case "2":
                installation()
            case "3":
                thermo_control()
            case "4":
                remote_control()
            case "5":
                calibration()
            case "6":
                schedule()
            case "7":
                milesight()
            case "8":
                external()
            case "9":
                screen()
            case "10":
                history()
            case "11":
                print("Exiting the program...\n")
                sleep(1)
                exit()
            case _:
                print("Invalid Input: Please try again!")
                sleep(1)

                
if __name__ == "__main__":
    main()