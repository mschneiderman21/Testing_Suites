import vicki_ttsApi
import time

def main():
    while True:
        payload = ""

        print("This program is used to get/send some of the common payloads used with the Vicki Smart Radiator Thermostat")
        print("\n What Payload do you want?")
        print("1. Reset")
        print("2. Set uplink inteerval")
        print("3. Set control mode")
        print("4. Set target temp")
        print("5. Send external temp")
        print("6. Child lock")
        print("7. Exit")
        
        match input("\nEnter your selection: "):
            case "1":
                payload = "30"
            case "2":
                interval = hex(int(input("\nEnter the desired uplink interval (1 to 255 minutes): ")))[2:]
                while len(interval) < 2: interval = "0" + interval

                payload = "02" + interval
            case "3":
                print("What control mode:")
                print("00 - Online manual control mode")
                print("01 - Online automatic control mode")
                print("02 - Online automatic control mode with external temperature reading")
                mode = input("\nEnter the desired control mode: ")

                while len(mode) < 2: mode = "0" + mode
                
                payload = "0d" + mode
                
            case "4":
                temp = hex(int(float(input("Enter the target temperature in Celsius: ")) * 10))[2:]  

                while len(temp) < 4: temp = "0" + temp

                payload = "51" + temp         
            case "5":
                temp = hex(int(float(input("Enter the temperature value in Celsius: ")) * 10))[2:]

                while len(temp) < 4: temp = "0" + temp

                payload = "3c" + temp    
            case "6":
                ch_lock = input("Enter 1 to enable or 0 to disable the child lock: ")
                while len(ch_lock) < 2: ch_lock = "0" + ch_lock

                payload = "07" + ch_lock
            case "7":
                print("Exiting the program.....BYE!......\n")
                time.sleep(1)
                exit()

            case _:
                print("Invalid Input: Please try again! \n")
                main()



        print("\nThe payload is: " + payload)
        match input("Do you want to send it to vicki? 1 -> Yes or 0 -> No: "):
            case "1":
                frm_payload = vicki_ttsApi.toBase64(payload)
                vicki_ttsApi.downlink(frm_payload)
                print("Payload delivered! Returning to main menu...\n")
                time.sleep(1)
            case _:
                print("Returning to the main menu...\n")
                time.sleep(1)





if __name__ == "__main__":
    main()