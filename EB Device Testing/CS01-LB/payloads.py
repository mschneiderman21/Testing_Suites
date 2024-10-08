import CS01_ttsAPI
import time

def main():
    while True:
        payload = ""

        print("This program is used to get/send some of the common payloads used with the Vicki Smart Radiator Thermostat")
        print("\n What Payload do you want?")
        print("1. Set uplink interval")
        print("2. Set interrupt mode")
        print("3. Set working mode")
        print("4. Set alarm threshold")
        print("5. Set alarm interval")
        print("6. Child lock")
        print("7. Exit")
        
        match input("\nEnter your selection: "):
            case "1":
                interval = hex(int(input("\nEnter the desired uplink interval (1 to 255 minutes): ")) * 60)[2:]
                while len(interval) < 6: interval = "0" + interval

                payload = "01" + interval
            case "2":
                print("This hasn't been implemented yet. Sorry.")
                main()
            case "3":
                print("This hasn't been implemented yet. Sorry.")
                main()
                
            case "4":
                alarm = input("Enter 0 to disable or 1 to enable the alarm: ")
                while len(alarm) < 2: alarm = "0" + alarm

                current1_type = input("Enter 0 for a below threshold or 1 for an above threshold: ")
                while len(current1_type) < 2: current1_type = "0" + current1_type

                threshold1 =  hex(int(input("Enter the desire thershold in Amps: ")))[2:]
                while len(threshold1) < 6: threshold1 = "0" + threshold1

                current2_type = input("Enter 0 for a below threshold or 1 for an above threshold: ")
                while len(current2_type) < 2: current2_type = "0" + current2_type

                threshold2 =  hex(int(input("Enter the desire thershold in Amps: ")))[2:]
                while len(threshold2) < 6: threshold2 = "0" + threshold2
             
                current3_type = input("Enter 0 for a below threshold or 1 for an above threshold: ")
                while len(current3_type) < 2: current3_type = "0" + current3_type

                threshold3 =  hex(int(input("Enter the desire thershold in Amps: ")))[2:]
                while len(threshold3) < 6: threshold3 = "0" + threshold3

                current4_type = input("Enter 0 for a below threshold or 1 for an above threshold: ")
                while len(current4_type) < 2: current4_type = "0" + current4_type

                threshold4 =  hex(int(input("Enter the desire thershold in Amps: ")))[2:]
                while len(threshold4) < 6: threshold4 = "0" + threshold4

                payload = "0b" + alarm + current1_type + threshold1 + current2_type + threshold2 + current3_type + threshold3+ current4_type + threshold4


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
                frm_payload = CS01_ttsAPI.toBase64(payload)
                CS01_ttsAPI.downlink(frm_payload)
                print("Payload delivered! Returning to main menu...\n")
                time.sleep(1)
            case _:
                print("Returning to the main menu...\n")
                time.sleep(1)





if __name__ == "__main__":
    main()