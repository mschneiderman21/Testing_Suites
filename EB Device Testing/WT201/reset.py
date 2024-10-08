import time
import tts_downlinks

def test_reset():
    print(f"Resetting the thermostat to Auto 22.8℃ and sending a temperature value of 22.8℃")
    reset = [("ffb703c9", 50), ("03e30000", 50), ("ff8e000100", 50), ("ffbd10ff", 50), ("ffc4010f", 50)]

    for tuple in reset:
        time.sleep(tuple[1])
        frm_payload = tts_downlinks.toBase64(tuple[0])
        tts_downlinks.downlink(frm_payload)
    print("Reset complete\n")
    time.sleep(60)

def enable_external_temp(timeout):
    payload = "ffc401"
    hex_time = hex(timeout)[2:]

    while len(hex_time) < 2: hex_time = "0" + hex_time

    payload = payload + hex_time

    frm_payload = tts_downlinks.toBase64(str(payload))
    tts_downlinks.downlink(frm_payload)