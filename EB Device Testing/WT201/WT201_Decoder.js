function decodeUplink(input) {
    var decoded = deviceDecode(input.bytes);
    return { data: decoded };
}

function deviceDecode(bytes) {
    var payload = {};
    var decoded = {payload};

    for (var i = 0; i < bytes.length; ) {
        var channel_id = bytes[i++];
        var channel_type = bytes[i++];

        // IPSO VERSION
        if (channel_id === 0xff && channel_type === 0x01) {
            decoded.ipso_version = readProtocolVersion(bytes[i]);
            i += 1;
        }
        // HARDWARE VERSION
        else if (channel_id === 0xff && channel_type === 0x09) {
            decoded.hardware_version = readHardwareVersion(bytes.slice(i, i + 2));
            i += 2;
        }
        // FIRMWARE VERSION
        else if (channel_id === 0xff && channel_type === 0x0a) {
            decoded.firmware_version = readFirmwareVersion(bytes.slice(i, i + 2));
            i += 2;
        }
        // DEVICE STATUS
        else if (channel_id === 0xff && channel_type === 0x0b) {
            decoded.device_status = "on";
            i += 1;
        }
        // LORAWAN CLASS TYPE
        else if (channel_id === 0xff && channel_type === 0x0f) {
            decoded.lorawan_class = readLoRaWANClass(bytes[i]);
            i += 1;
        }
        // PRODUCT SERIAL NUMBER
        else if (channel_id === 0xff && channel_type === 0x16) {
            decoded.sn = readSerialNumber(bytes.slice(i, i + 8));
            i += 8;
        }
        // TSL VERSION
        else if (channel_id === 0xff && channel_type === 0xff) {
            decoded.tsl_version = readFirmwareVersion(bytes.slice(i, i + 2));
            i += 2;
        }
        // TEMPERATURE
        else if (channel_id === 0x03 && channel_type === 0x67) {
            payload.temp = Math.round(((readInt16LE(bytes.slice(i, i + 2)) / 10) * 1.8 + 32) * 10) / 10;
            i += 2;
        }
        // TEMPERATURE TARGET
        else if (channel_id === 0x04 && channel_type === 0x67) {
            payload.ind_sp_act = Math.round(((readInt16LE(bytes.slice(i, i + 2)) / 10) * 1.8 + 32) * 10) / 10;
            i += 2;
        }
        // TEMPERATURE CONTROL
        else if (channel_id === 0x05 && channel_type === 0xe7) {
            var temperature_control = bytes[i];
            payload.ctrl_mode = readTemperatureCtlMode(temperature_control & 0x03);
            payload.ctrl_status = readTemperatureCtlStatus((temperature_control >>> 4) & 0x0f);
            i += 1;
        }
        // FAN CONTROL
        else if (channel_id === 0x06 && channel_type === 0xe8) {
            var value = bytes[i];
            payload.fan_mode = readFanMode(value & 0x03);
            payload.fan_rs = readFanStatus((value >>> 2) & 0x03);
            i += 1;
        }
        // PLAN EVENT
        else if (channel_id === 0x07 && channel_type === 0xbc) {
            var value = bytes[i];
            payload.cur_mode = readPlanEvent(value & 0x0f);
            i += 1;
        }
        // SYSTEM STATUS
        else if (channel_id === 0x08 && channel_type === 0x8e) {
            payload.tstat_status = readSystemStatus(bytes[i]);
            i += 1;
        }
        // HUMIDITY
        else if (channel_id === 0x09 && channel_type === 0x68) {
            payload.humidity = readUInt8(bytes[i]) / 2;
            i += 1;
        }
        // RELAY STATUS
        else if (channel_id === 0x0a && channel_type === 0x6e) {
            decoded.wires_relay = readWiresRelay(bytes[i]);
            i += 1;
        }
        // PLAN
        else if (channel_id === 0xff && channel_type === 0xc9) {
            var schedule = {};
            schedule.type = readPlanType(bytes[i]);
            schedule.index = bytes[i + 1] + 1;
            schedule.plan_enable = ["disable", "enable"][bytes[i + 2]];
            schedule.week_recycle = readWeekRecycleSettings(bytes[i + 3]);
            var time_mins = readUInt16LE(bytes.slice(i + 4, i + 6));
            schedule.time = Math.floor(time_mins / 60) + ":" + ("0" + (time_mins % 60)).slice(-2);
            i += 6;

            decoded.plan_schedule = decoded.plan_schedule || [];
            decoded.plan_schedule.push(schedule);
        }
        // PLAN SETTINGS
        else if (channel_id === 0xff && channel_type === 0xc8) {
            var plan_setting = {};
            plan_setting.type = readPlanType(bytes[i]);
            plan_setting.ctrl_mode = readTemperatureCtlMode(bytes[i + 1]);
            plan_setting.fan_mode = readFanMode(bytes[i + 2]);
            plan_setting.ind_sp_act = readUInt8(bytes[i + 3] & 0x7f);
            plan_setting.temp_unit = readTemperatureUnit(bytes[i + 3] >>> 7);
            plan_setting.temp_error = readUInt8(bytes[i + 4]) / 10;
            i += 5;

            decoded.plan_settings = decoded.plan_settings || [];
            decoded.plan_settings.push(plan_setting);
        }
        // WIRES
        else if (channel_id === 0xff && channel_type === 0xca) {
            decoded.wires = readWires(bytes[i], bytes[i + 1], bytes[i + 2]);
            decoded.ob_mode = readObMode((bytes[i + 2] >>> 2) & 0x03);
            i += 3;
        }
        // TEMPERATURE MODE SUPPORT
        else if (channel_id === 0xff && channel_type === 0xcb) {
            decoded.ctrl_mode_enable = readTemperatureCtlModeEnable(bytes[i]);
            decoded.ctrl_status_enable = readTemperatureCtlStatusEnable(bytes[i + 1], bytes[i + 2]);
            i += 3;
        }
        // CONTROL PERMISSIONS
        else if (channel_id === 0xff && channel_type === 0xf6) {
            decoded.control_permissions = bytes[i] === 1 ? "Remote" : "Thermostat";
            i += 1;
        }
        // TEMPERATURE ALARM
        else if (channel_id === 0x83 && channel_type === 0x67) {
            decoded.temp = readInt16LE(bytes.slice(i, i + 2)) / 10;
            decoded.alarm = readTemperatureAlarm(bytes[i + 2]);
            i += 2;
        }
        // TEMPERATURE EXCEPTION
        else if (channel_id === 0xb3 && channel_type === 0x67) {
            decoded.temp_exception = readException(bytes[i]);
            i += 1;
        }
        // HUMIDITY EXCEPTION
        else if (channel_id === 0xb9 && channel_type === 0x68) {
            decoded.humidity_exception = readException(bytes[i]);
            i += 1;
        }
        // HISTORICAL DATA
        else if (channel_id === 0x20 && channel_type === 0xce) {
            var timestamp = readUInt32LE(bytes.slice(i, i + 4));
            var value1 = readUInt16LE(bytes.slice(i + 4, i + 6));
            var value2 = readUInt16LE(bytes.slice(i + 6, i + 8));

            var data = { timestamp: timestamp };
            // fan_mode(0..1) + fan_status(2..3) + system_status(4) + temperature(5..15)
            data.fan_mode = readFanMode(value1 & 0x03);
            data.fan_rs = readFanStatus((value1 >>> 2) & 0x03);
            data.tstat_status = readSystemStatus((value1 >>> 4) & 0x01);
            var temperature = ((value1 >>> 5) & 0x7ff) / 10 - 100;
            data.temp = Number(temperature.toFixed(1));

            // temperature_ctl_mode(0..1) + temperature_ctl_status(2..4) + temperature_target(5..15)
            data.temperature_ctl_mode = readTemperatureCtlMode(value2 & 0x03);
            data.temperature_ctl_status = readTemperatureCtlStatus((value2 >>> 2) & 0x07);
            var temperature_target = ((value2 >>> 5) & 0x7ff) / 10 - 100;
            data.temperature_target = Number(temperature_target.toFixed(1));
            i += 8;

            decoded.history = decoded.history || [];
            decoded.history.push(data);
        }
        // DOWNLINK RESPONSE
        else if (channel_id === 0xfe) {
            result = handle_downlink_response(channel_type, bytes, i);
            decoded = Object.assign(decoded, result.data);
            i = result.offset;
        } else if (channel_id === 0xf8) {
            result = handle_downlink_response_ext(channel_type, bytes, i);
            decoded = Object.assign(decoded, result.data);
            i = result.offset;
        } else {
            break;
        }
    }

    return decoded;
}

function readUInt8(bytes) {
    return bytes & 0xff;
}

function readInt8(bytes) {
    var ref = readUInt8(bytes);
    return ref > 0x7f ? ref - 0x100 : ref;
}

function readUInt16LE(bytes) {
    var value = (bytes[1] << 8) + bytes[0];
    return value & 0xffff;
}

function readInt16LE(bytes) {
    var ref = readUInt16LE(bytes);
    return ref > 0x7fff ? ref - 0x10000 : ref;
}

function readUInt32LE(bytes) {
    var value = (bytes[3] << 24) + (bytes[2] << 16) + (bytes[1] << 8) + bytes[0];
    return (value & 0xffffffff) >>> 0;
}

function readInt32LE(bytes) {
    var ref = readUInt32LE(bytes);
    return ref > 0x7fffffff ? ref - 0x100000000 : ref;
}

function readProtocolVersion(bytes) {
    var major = (bytes & 0xf0) >> 4;
    var minor = bytes & 0x0f;
    return "v" + major + "." + minor;
}

function readHardwareVersion(bytes) {
    var major = bytes[0] & 0xff;
    var minor = (bytes[1] & 0xff) >> 4;
    return "v" + major + "." + minor;
}

function readFirmwareVersion(bytes) {
    var major = bytes[0] & 0xff;
    var minor = bytes[1] & 0xff;
    return "v" + major + "." + minor;
}

function readSerialNumber(bytes) {
    var temp = [];
    for (var idx = 0; idx < bytes.length; idx++) {
        temp.push(("0" + (bytes[idx] & 0xff).toString(16)).slice(-2));
    }
    return temp.join("");
}

function readD2DCommand(bytes) {
    return ("0" + (bytes[1] & 0xff).toString(16)).slice(-2) + ("0" + (bytes[0] & 0xff).toString(16)).slice(-2);
}

function readLoRaWANClass(type) {
    switch (type) {
        case 0x00:
            return "ClassA";
        case 0x01:
            return "ClassB";
        case 0x02:
            return "ClassC";
        case 0x03:
            return "ClassCtoB";
        default:
            return "unknown";
    }
}

function readTemperatureUnit(type) {
    switch (type) {
        case 0x00:
            return "℃";
        case 0x01:
            return "℉";
        default:
            return "unknown";
    }
}

function readTemperatureAlarm(type) {
    // 1: emergency heating timeout alarm, 2: auxiliary heating timeout alarm, 3: persistent low temperature alarm, 4: persistent low temperature alarm release,
    // 5: persistent high temperature alarm, 6: persistent high temperature alarm release, 7: freeze protection alarm, 8: freeze protection alarm release,
    // 9: threshold alarm, 10: threshold alarm release
    switch (type) {
        case 0x01:
            return "emergency heating timeout alarm";
        case 0x02:
            return "auxiliary heating timeout alarm";
        case 0x03:
            return "persistent low temperature alarm";
        case 0x04:
            return "persistent low temperature alarm release";
        case 0x05:
            return "persistent high temperature alarm";
        case 0x06:
            return "persistent high temperature alarm release";
        case 0x07:
            return "freeze protection alarm";
        case 0x08:
            return "freeze protection alarm release";
        case 0x09:
            return "threshold alarm";
        case 0x0a:
            return "threshold alarm release";
        default:
            return "unknown";
    }
}

function readException(type) {
    switch (type) {
        case 0x01:
            return "Fail";
        case 0x02:
            return "OutOfRange";
        default:
            return "unknown";
    }
}

function readPlanEvent(type) {
    // 0: not executed, 1: wake, 2: away, 3: home, 4: sleep
    switch (type) {
        case 0x00:
            return 0;
        case 0x01:
            return 1;
        case 0x02:
            return 2;
        case 0x03:
            return 3;
        case 0x04:
            return 4;
        default:
            return 5;
    }
}

function readPlanType(type) {
    // 1: wake, 2: away, 3: home, 4: sleep
    switch (type) {
        case 0x00:
            return 1;
        case 0x01:
            return 2;
        case 0x02:
            return 3;
        case 0x03:
            return 4;
        default:
            return 5;
    }
}

function readFanMode(type) {
    // 0: auto, 1: on, 2: circulate, 3: disable
    switch (type) {
        case 0x00:
            return 0;
        case 0x01:
            return 1;
        case 0x02:
            return 2;
        case 0x03:
            return 3;
        default:
            return 4;
    }
}

function readFanStatus(type) {
    // 0: standby, 1: high speed, 2: low speed, 3: on
    switch (type) {
        case 0x00:
            return 0;
        case 0x01:
            return 1;
        case 0x02:
            return 2;
        case 0x03:
            return 3;
        default:
            return 4;
    }
}

function readSystemStatus(type) {
    // 0: off, 1: on
    switch (type) {
        case 0x00:
            return "off";
        case 0x01:
            return "on";
        default:
            return "unknown";
    }
}

function readTemperatureCtlMode(type) {
    // 0: heat, 1: em heat, 2: cool, 3: auto
    switch (type) {
        case 0x00:
            return 0;
        case 0x01:
            return 1;
        case 0x02:
            return 2;
        case 0x03:
            return 3;
        default:
            return 4;
    }
}

function readTemperatureCtlStatus(type) {
    // 0: standby, 1: stage-1 heat, 2: stage-2 heat, 3: stage-3 heat, 4: stage-4 heat, 5: em heat, 6: stage-1 cool, 7: stage-2 cool
    switch (type) {
        case 0x00:
            return 0;
        case 0x01:
            return 1;
        case 0x02:
            return 2;
        case 0x03:
            return 3;
        case 0x04:
            return 4;
        case 0x05:
            return 5;
        case 0x06:
            return 6;
        case 0x07:
            return 7;
        default:
            return 8;
    }
}

function readWires(wire1, wire2, wire3) {
    var wire = [];
    if ((wire1 >>> 0) & 0x03) {
        wire.push("Y1");
    }
    if ((wire1 >>> 2) & 0x03) {
        wire.push("GH");
    }
    if ((wire1 >>> 4) & 0x03) {
        wire.push("OB");
    }
    if ((wire1 >>> 6) & 0x03) {
        wire.push("W1");
    }
    if ((wire2 >>> 0) & 0x03) {
        wire.push("E");
    }
    if ((wire2 >>> 2) & 0x03) {
        wire.push("DI");
    }
    if ((wire2 >>> 4) & 0x03) {
        wire.push("PEK");
    }
    var w2_aux_wire = (wire2 >>> 6) & 0x03;
    switch (w2_aux_wire) {
        case 1:
            wire.push("W2");
            break;
        case 2:
            wire.push("AUX");
            break;
    }
    var y2_gl_wire = (wire3 >>> 0) & 0x03;
    switch (y2_gl_wire) {
        case 1:
            wire.push("Y2");
            break;
        case 2:
            wire.push("GL");
            break;
    }

    return wire;
}

function readWiresRelay(status) {
    var relay = {};
    
    relay.y1 = (status >>> 0) & 0x01;
    relay.y2_gl = (status >>> 1) & 0x01;
    relay.w1 = (status >>> 2) & 0x01;
    relay.w2_aux = (status >>> 3) & 0x01;
    relay.e = (status >>> 4) & 0x01;
    relay.g = (status >>> 5) & 0x01;
    relay.ob = (status >>> 6) & 0x01;

    return relay;
}

function readObMode(type) {
    // 0: cool, 1: heat
    switch (type) {
        case 0x00:
            return "cool";
        case 0x01:
            return "heat";
        default:
            return "unknown";
    }
}

function readTemperatureCtlModeEnable(type) {
    // bit0: heat, bit1: em heat, bit2: cool, bit3: auto
    var enable = [];
    if ((type >>> 0) & 0x01) {
        enable.push("heat");
    }
    if ((type >>> 1) & 0x01) {
        enable.push("em heat");
    }
    if ((type >>> 2) & 0x01) {
        enable.push("cool");
    }
    if ((type >>> 3) & 0x01) {
        enable.push("auto");
    }
    return enable;
}

function readTemperatureCtlStatusEnable(heat_mode, cool_mode) {
    // bit0: stage-1 heat, bit1: stage-2 heat, bit2: stage-3 heat, bit3: stage-4 heat, bit4: aux heat
    var enable = [];
    if ((heat_mode >>> 0) & 0x01) {
        enable.push("stage-1 heat");
    }
    if ((heat_mode >>> 1) & 0x01) {
        enable.push("stage-2 heat");
    }
    if ((heat_mode >>> 2) & 0x01) {
        enable.push("stage-3 heat");
    }
    if ((heat_mode >>> 3) & 0x01) {
        enable.push("stage-4 heat");
    }
    if ((heat_mode >>> 4) & 0x01) {
        enable.push("aux heat");
    }

    // bit0: stage-1 cool, bit1: stage-2 cool
    if ((cool_mode >>> 0) & 0x03) {
        enable.push("stage-1 cool");
    }
    if ((cool_mode >>> 1) & 0x03) {
        enable.push("stage-2 cool");
    }
    return enable;
}

function readWeekRecycleSettings(type) {
    // bit1: "mon", bit2: "tues", bit3: "wed", bit4: "thur", bit5: "fri", bit6: "sat", bit7: "sun"
    var week_enable = [];
    if ((type >>> 1) & 0x01) {
        week_enable.push("Mon.");
    }
    if ((type >>> 2) & 0x01) {
        week_enable.push("Tues.");
    }
    if ((type >>> 3) & 0x01) {
        week_enable.push("Wed.");
    }
    if ((type >>> 4) & 0x01) {
        week_enable.push("Thur.");
    }
    if ((type >>> 5) & 0x01) {
        week_enable.push("Fri.");
    }
    if ((type >>> 6) & 0x01) {
        week_enable.push("Sat.");
    }
    if ((type >>> 7) & 0x01) {
        week_enable.push("Sun.");
    }
    return week_enable;
}

console.log(decodeUplink({bytes: [0x03, 0x67, 0xEE, 0x00, 0x08, 0x8E, 0x01, 0x04, 0x67, 0xD3, 0x00, 0x05, 0xE7, 0x00, 0x06, 0xE8, 0x0D, 0x07, 0xBC, 0x00]}))

// console.log(decodeUplink({bytes: [0xFF, 0x0B, 0xFF, 0xFF, 0x01, 0x01, 0xFF, 0x16, 0x67, 0x15, 0xD4, 0x83, 0x23, 0x17, 0x00, 0x00, 0xFF, 0x09, 0x01, 0x10, 0xFF, 0x0A, 0x01, 0x03, 0xFF, 0x0F, 0x02, 0xFF, 0xFF, 0x01, 0x00, 0xFF, 0xCB, 0x0D, 0x07, 0x03, 0xFF, 0xCA, 0x55, 0x00, 0x05]}))


