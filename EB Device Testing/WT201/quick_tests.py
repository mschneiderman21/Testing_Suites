import time 
import tts_downlinks
import reset
import support
import sinTemp

time_int = 50

def main():

    # # test = [("03e30000", 50),         ("ffb702c6", 50),
    # #     ("03e20000", 0), ("03e10000", time_int), ("03e00000", time_int), ("03e00000", time_int), ("03df0000", time_int), 
    # #     ("03e00000", time_int), ("03df0000", time_int), ("03dd0000", time_int), ("03dc0000", time_int), ("03db0000", time_int),        
    # #     ("03d90000", time_int), ("03d70000", time_int), ("03d60000", time_int), ("03d40000", time_int), ("03d50000", time_int),
    # #     ("03d40000", time_int), ("03d30000", time_int), ("03d40000", time_int), ("03d30000", time_int), ("03d20000", time_int)]
    
    # test =[("03D70000", 0),  ("ffb702c6", 5),
    #     ("03D70000", time_int), ("03D60000", time_int), ("03D50000", time_int), ("03D40000", time_int), 
    #     ("03D30000", time_int), ("03D20000", time_int), ("03D30000", time_int), ("03D20000", time_int),
    #     ("03D30000", time_int), ("03D20000", time_int), ("03D30000", time_int), ("03D20000", time_int), 
    #     ("03D30000", time_int), ("03D20000", time_int), ("03D30000", time_int), ("03D20000", time_int)]
    
    # reset.enable_external_temp(10)

    # reset.test_reset()

    # time.sleep(50)
    

    # for tuple in test:
    #     time.sleep(tuple[1])
    #     frm_payload = tts_downlinks.toBase64(tuple[0])
    #     tts_downlinks.downlink(frm_payload)
    #     print("Payload Delivered")

    print("The program started running")


    test = [("03c80000", 50), ("fff601", 50), ("fff600", 120), ("ffb702c0", 50), ("fff601", 50),]
    for tuple in test:
        time.sleep(tuple[1])
        frm_payload = tts_downlinks.toBase64(tuple[0])
        tts_downlinks.downlink(frm_payload)
    
    print("The program finished running")
    


if __name__ == "__main__":
    main()
