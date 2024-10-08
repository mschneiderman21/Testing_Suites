import EM320_TILT_ttsApi
import time

def main():
    while True:
        payload = ""

        print("This program is used to get/send the payloads used with the EM320 TILT")
        print("\n What Payload do you want?")
        print("1. Reboot")
        print("2. Set uplink interval")
        print("3. Set Threshold")
        print("4. Set Initial Position")
        print("5. Exit")
        
        match input("\nEnter your selection: "):
            case "1":
                payload = "ff10ff"
            case "2":
                interval = hex(int(input("\nEnter the desired uplink interval in seconds: ")))[2:]
                while len(interval) < 4: interval = "0" + interval

                payload = "ff03" + interval
                print(payload)
            case "3":
                print("What is the Threshold Type?")
                print("0 - Disable")
                print("1 - Below (Minimum Threshold)")
                print("2 - Over (Maximum Threshold)")
                print("3 - Within")
                print("4 - Below or Above")
                
                mode = bin(int(input("\nEnter the desired Threshold Type: ")))[2:]

                while len(mode) < 3: mode = "0" + mode

                print("What axis is is the threshold for?")
                print("0 - X")
                print("1 - Y ")
                print("2 - Z")

                match input("\nEnter the desire axis: "):

                    case "0":
                        axis = "001"
                    case "1":
                        axis = "010"
                    case "2":
                        axis = "100"
                    case _:
                        print("Invalid Input: Please try again! \n")
                        main()
                threshold = "00" + axis + mode
                threshold = hex(int(threshold, 2))[2:]

                while len(threshold) < 3: threshold = "0" + threshold

                min = hex(int(input("\nEnter the minimum threshold (1000 -> 10.00 degrees): ")))[2:]
                while len(min) < 4: min = "0" + min
                min = min[2:] + min[:2] 

                max = hex(int(input("\nEnter the maximum threshold (1000 -> 10.00 degrees): ")))[2:]
                while len(max) < 4: max = "0" + max
                max = max[2:] + max[:2]

                interval = hex(int(input("\nEnter the alarm reporting interval in seconds: ")))[2:]
                while len(interval) < 4: interval = "0" + interval
                interval = interval[2:] + interval[:2]

                reports = hex(int(input("\nEnter the number of times the alarm should be reported: ")))[2:]
                while len(reports) < 4: reports = "0" + reports
                reports = reports[2:] + reports[:2]
                
                payload = "ff06" + threshold + min + max + interval + reports

            case "4":
                print("ff -  Set current position as initial position") 
                print("fe -  Set the initial position to (0.00°, 0.00°, -90.00°)") 
                choice = input("Enter your selection: ")

                payload = "ff62" + choice            
            case "5":
                print("Exiting the program.....BYE!......\n")
                time.sleep(1)
                exit()

            case _:
                print("Invalid Input: Please try again! \n")
                main()



        print("\nThe payload is: " + payload)
        match input("Do you want to send it to EM320 TILT? 1 -> Yes or 0 -> No: "):
            case "1":
                frm_payload = EM320_TILT_ttsApi.toBase64(payload)
                EM320_TILT_ttsApi.downlink(frm_payload)
                print("Payload delivered! Returning to main menu...\n")
                time.sleep(1)
            case _:
                print("Returning to the main menu...\n")
                time.sleep(1)





if __name__ == "__main__":
    main()