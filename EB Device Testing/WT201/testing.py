import time
import tts_downlinks
import datetime
import pytz
import reset

time_int = 55
test_num = 0
time_zone = pytz.timezone("America/New_York")


def main():
    global test_num

    # TESTING DESCRIPTION: Testing the wt201 smart thermostat cooling algorithm. Testing convergence to the target temperature.
    # TESTING SETTINGS: Cooling rate of .1 C every 5 minutes till it dips below target at 21C
    #       Send temp of 22.7C ~ 73F / Cool 70F ~ 21.1C
    test_0 = [("03e30000", 0), ("ffb702c6", 50),
              ('03d20000', 0), ('03d30000', time_int), ('03d40000', time_int), ('03d50000', time_int), ('03d60000', time_int), ('03d70000', time_int),
              ('03d80000', time_int), ('03d90000', time_int), ('03da0000', time_int), ('03db0000', time_int), ('03dc0000', time_int), 
              ('03dd0000', time_int), ('03de0000', time_int), ('03df0000', time_int), ('03df0000', time_int), ('03df0000', time_int)]

    # # TESTING DESCRIPTION: Testing the wt201 smart thermostat cooling algorithm. Testing divergence to the target temperature.
    # # TESTING SETTINGS: Cooling rate of about -.1 C every 5 minutes till it reaches 24C
    # #        Send temp of 22.8C ~ 73F /  Cool 70F ~ 21.1C
    # test_1 = [("03e40000", 50),         ("ffb702c6", 50),
    #     ("03e30000", time_int), ("03e40000", time_int), ("03e50000", time_int), ("03e40000", time_int), ("03e50000", time_int),
    #     ("03e60000", time_int), ("03e70000", time_int), ("03e60000", time_int), ("03e70000", time_int), ("03e80000", time_int),
    #     ("03e90000", time_int), ("03ea0000", time_int), ("03e80000", time_int), ("03ea0000", time_int), ("03ec0000", time_int),
    #     ("03ee0000", time_int), ("03ef0000", time_int), ("03f00000", time_int), ("03ef0000", time_int), ("03f00000", time_int)]

    # # TESTING DESCRIPTION: Testing the wt201 smart thermostat cooling algorithm. Testing flatlining to the target temperature.
    # # TESTING SETTINGS: The target temp is 21.1 however it will stay at 22.8C and will fluctuate by +-.3C
    # #        Send temp of 22.8C ~ 73F / Cool 70F ~ 21.1C
    # test_2 = [("03e40000", 50),         ("ffb702c6", 50),
    #     ("03e30000", time_int), ("03e20000", time_int), ("03e10000", time_int), ("03e10000", time_int), ("03e20000", time_int),
    #     ("03e30000", time_int), ("03e40000", time_int), ("03e50000", time_int), ("03e40000", time_int), ("03e20000", time_int),
    #     ("03e30000", time_int), ("03e40000", time_int), ("03e50000", time_int), ("03e60000", time_int), ("03e50000", time_int),
    #     ("03e40000", time_int), ("03e30000", time_int), ("03e20000", time_int), ("03e30000", time_int), ("03e40000", time_int)]

    # # TESTING DESCRIPTION: Testing the wt201 smart thermostat heating algorithm. Testing comvergence to the target temperature.
    # # TESTING SETTINGS: Heating rate of about .1 C every 5 minutes till it reaches 23.3C
    # #         Send temp of 22.8C ~ 73F / Heat 75F ~ 23.9C
    # test_3 = [("03e40000", 50),         ("ffb700cb", 50),
    #     ("03e30000", time_int), ("03e40000", time_int), ("03e50000", time_int), ("03e40000", time_int), ("03e50000", time_int),
    #     ("03e60000", time_int), ("03e70000", time_int), ("03e60000", time_int), ("03e70000", time_int), ("03e80000", time_int),
    #     ("03e90000", time_int), ("03ea0000", time_int), ("03e80000", time_int), ("03ea0000", time_int), ("03ec0000", time_int),
    #     ("03ee0000", time_int), ("03ef0000", time_int), ("03f00000", time_int), ("03ef0000", time_int), ("03f00000", time_int)]

    # # TESTING DESCRIPTION: Testing the wt201 smart thermostat heating algorithm. Testing divergence to the target temperature.
    # # TESTING SETTINGS: Heating rate of about -.1 C every 5 minutes till it dips below target at 21C
    # #       Send temp of 22.8C ~ 73F / Heat 75F ~ 23.9C
    # test_4 = [("03e40000", 50),         ("ffb700cb", 50),
    #     ("03e30000", time_int), ("03e20000", time_int), ("03e10000", time_int), ("03e00000", time_int), ("03df0000", time_int),
    #     ("03e00000", time_int), ("03df0000", time_int), ("03dd0000", time_int), ("03dc0000", time_int), ("03db0000", time_int),
    #     ("03d90000", time_int), ("03d70000", time_int), ("03d60000", time_int), ("03d40000", time_int), ("03d50000", time_int),
    #     ("03d40000", time_int), ("03d30000", time_int), ("03d40000", time_int), ("03d30000", time_int), ("03d20000", time_int)]

    # # TESTING DESCRIPTION: Testing the wt201 smart thermostat heating algorithm. Testing divergence to the target temperature.
    # # TESTING SETTINGS: Heating rate of about -.1 C every 5 minutes till it dips below target at 21C
    # #          Send temp of 22.8C ~ 73F / Heat 75F ~ 23.9C
    # test_5 = [("03e40000", 50),          ("ffb700cb", 50),
    #     ("03e30000", time_int), ("03e20000", time_int), ("03e10000", time_int), ("03e10000", time_int), ("03e20000", time_int),
    #     ("03e30000", time_int), ("03e40000", time_int), ("03e50000", time_int), ("03e40000", time_int), ("03e20000", time_int),
    #     ("03e30000", time_int), ("03e40000", time_int), ("03e50000", time_int), ("03e60000", time_int), ("03e50000", time_int),
    #     ("03e40000", time_int), ("03e30000", time_int), ("03e20000", time_int), ("03e30000", time_int), ("03e40000", time_int)]

    tests = [test_0]

    # Wait untill 8 PM to start testing

    print(f"The testing began at {datetime.datetime.now()}")
    for test in tests:
        #reset.test_reset()
        tot_num_downlinks = len(test)
        num_downlinks_sent = 1
        print(f"Started running test #{test_num} at: {datetime.datetime.now()}")
        for tuple in test:
            time.sleep(tuple[1])
            frm_payload = tts_downlinks.toBase64(tuple[0])
            tts_downlinks.downlink(frm_payload)

            print(f"{num_downlinks_sent}/{tot_num_downlinks} sent...")
            num_downlinks_sent += 1
        print(f"Finished running test #{test_num} at: {datetime.datetime.now()}")

    test_num += 1

    # 5 Minute Delay Between Tests
    time.sleep(300)

    print(f"The Program finished running at: {datetime.datetime.now()}")


def wait_until():
    now = datetime.datetime.now(time_zone)
    next = (now + datetime.timedelta(days=0)).replace(hour=20,
                                                      minute=0, second=0, microsecond=0)
    time_till_start = (next - now).total_seconds()
    print(f"Waiting for {time_till_start} seconds until start.")
    time.sleep(time_till_start + 120)
    print("It's Time! Starting the program...")


if __name__ == "__main__":
    main()
