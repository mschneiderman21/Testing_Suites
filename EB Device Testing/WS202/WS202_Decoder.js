
function decodeUplink(input) {
    var bytes = input.bytes
    var payload = {};
    var decoded = {payload};

    for (var i = 0; i < bytes.length; ) {
        var channel_id = bytes[i++];
        var channel_type = bytes[i++];
        // BATTERY
        if (channel_id === 0x01 && channel_type === 0x75) {
            payload.battery = bytes[i];
            i += 1;
        }
        // PIR
        else if (channel_id === 0x03 && channel_type === 0x00) {
            payload.room = bytes[i] === 0 ? "Empty" : "Occupied";
            i += 1;
        }
        // DAYLIGHT
        else if (channel_id === 0x04 && channel_type === 0x00) {
            payload.lights = bytes[i] === 0 ? "On" : "Off";
            i += 1;
        } else {
            break;
        }
    }

    return decoded;
}

console.log(decodeUplink({bytes: [0x01, 0x75, 0x64, 0x03, 0x00, 0x01, 0x04, 0x00, 0x01]}))
