import testing
import tts_downlinks
import time

time_int = 55

def main():
    num_downlinks_sent = 1
    testing.test_reset()

    test_1 = [("03e40000", 50),         ("ffb702c6", 50), 
        ("03e30000", time_int), ("03e40000", time_int), ("03e50000", time_int), ("03e40000", time_int), ("03e50000", time_int), 
        ("03e60000", time_int), ("03e70000", time_int), ("03e60000", time_int), ("03e70000", time_int), ("03e80000", time_int),        
        ("03e90000", time_int), ("03ea0000", time_int), ("03e80000", time_int), ("03ea0000", time_int), ("03ec0000", time_int),
        ("03ee0000", time_int), ("03ef0000", time_int), ("03f00000", time_int), ("03ef0000", time_int), ("03f00000", time_int)]

    for tuple in test_1:
        time.sleep(tuple[1])
        frm_payload = tts_downlinks.toBase64(tuple[0])
        tts_downlinks.downlink(frm_payload)
        print(f"{num_downlinks_sent}/{len(test_1)} sent...")
        num_downlinks_sent += 1
    
    print("TEST IS COMPLETE")

if __name__ == "__main__":
    main()