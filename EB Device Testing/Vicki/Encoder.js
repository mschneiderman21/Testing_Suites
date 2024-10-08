function encodeDownlink(input) {
  var bytes = [];
  for (let key of Object.keys(input.data)) {
    switch (key) {
      case "setKeepAlive": {
        bytes.push(0x02);
        bytes.push(input.data.setKeepAlive);
        break;
      }
      case "getKeepAliveTime": {
        bytes.push(0x12);
        break;
      }
      case "recalibrateMotor": {
        bytes.push(0x03);
        break;
      }
      case "getDeviceVersions": {
        bytes.push(0x04);
        break;
      }
      case "setOpenWindow": {
        let enabled = Number(input.data.setOpenWindow.enabled);
        let closeTime = parseInt(input.data.setOpenWindow.closeTime / 5);
        let delta = parseInt(input.data.setOpenWindow.delta, 8);
        let motorPosition = input.data.setOpenWindow.motorPosition;
        let motorPositionFirstPart = motorPosition & 0xff;
        let motorPositionSecondPart = (motorPosition >> 8) & 0xff;
        bytes.push(0x06);
        bytes.push(enabled);
        bytes.push(closeTime);
        bytes.push(motorPositionFirstPart);
        bytes.push((motorPositionSecondPart << 4) | delta);
        break;
      }

      case "getOpenWindowParams": {
        bytes.push(0x13);
        break;
      }
      case "setChildLock": {
        bytes.push(0x07);
        bytes.push(Number(input.data.setChildLock));
        break;
      }
      case "getChildLock": {
        bytes.push(0x14);
        break;
      }
      case "setTemperatureRange": {
        bytes.push(0x08);
        bytes.push(input.data.setTemperatureRange.min);
        bytes.push(input.data.setTemperatureRange.max);
        break;
      }
      case "getTemperatureRange": {
        bytes.push(0x15);
        break;
      }
      case "forceClose": {
        bytes.push(0x0b);
        break;
      }
      case "setInternalAlgoParams": {
        bytes.push(0x0c);
        bytes.push(input.data.setInternalAlgoParams.pFirstLast);
        bytes.push(input.data.setInternalAlgoParams.pNext);
        break;
      }
      case "getInternalAlgoParams": {
        bytes.push(0x16);
        break;
      }
      case "setInternalAlgoTdiffParams": {
        bytes.push(0x1a);
        bytes.push(input.data.setInternalAlgoTdiffParams.cold);
        bytes.push(input.data.setInternalAlgoTdiffParams.warm);
        break;
      }
      case "getInternalAlgoTdiffParams": {
        bytes.push(0x17);
        break;
      }
      case "setOperationalMode": {
        bytes.push(0x0d);
        bytes.push(input.data.setOperationalMode);
        break;
      }
      case "getOperationalMode": {
        bytes.push(0x18);
        break;
      }
      case "setTargetTemperature": {
        bytes.push(0x0e);
        bytes.push(input.data.setTargetTemperature);
        break;
      }
      case "setExternalTemperature": {
        bytes.push(0x0f);
        bytes.push(input.data.setExternalTemperature);
        break;
      }
      case "setJoinRetryPeriod": {
        // period should be passed in minutes
        let periodToPass = (input.data.setJoinRetryPeriod * 60) / 5;
        periodToPass = int(periodToPass);
        bytes.push(0x10);
        bytes.push(periodToPass);
        break;
      }
      case "getJoinRetryPeriod": {
        bytes.push(0x19);
        break;
      }
      case "setUplinkType": {
        bytes.push(0x11);
        bytes.push(input.data.setUplinkType);
        break;
      }
      case "getUplinkType": {
        bytes.push(0x1b);
        break;
      }
      case "setTargetTemperatureAndMotorPosition": {
        bytes.push(0x31);
        bytes.push(
          input.data.setTargetTemperatureAndMotorPosition.motorPosition
        );
        bytes.push(
          input.data.setTargetTemperatureAndMotorPosition.targetTemperature
        );
        break;
      }
      case "setWatchDogParams": {
        bytes.push(0x1c);
        bytes.push(input.data.setWatchDogParams.confirmedUplinks);
        bytes.push(input.data.setWatchDogParams.unconfirmedUplinks);
        break;
      }
      case "getWatchDogParams": {
        bytes.push(0x1d);
        break;
      }
      case "setPrimaryOperationalMode": {
        bytes.push(0x1e);
        bytes.push(input.data.setPrimaryOperationalMode);
        break;
      }
      case "getPrimaryOperationalMode": {
        bytes.push(0x1f);
        break;
      }
      case "setProportionalAlgorithmParameters": {
        bytes.push(0x2a);
        bytes.push(input.data.setProportionalAlgorithmParameters.coefficient);
        bytes.push(input.data.setProportionalAlgorithmParameters.period);
        break;
      }
      case "getProportionalAlgorithmParameters": {
        bytes.push(0x29);
        break;
      }
      case "setTemperatureControlAlgorithm": {
        bytes.push(0x2c);
        bytes.push(input.data.setTemperatureControlAlgorithm);
        break;
      }
      case "getTemperatureControlAlgorithm": {
        bytes.push(0x2b);
        break;
      }
      case "setMotorPositionOnly": {
        let motorPosition = input.data.setMotorPositionOnly;
        let motorPositionFirstPart = motorPosition & 0xff;
        let motorPositionSecondPart = (motorPosition >> 8) & 0xff;
        bytes.push(0x2d);
        bytes.push(motorPositionSecondPart);
        bytes.push(motorPositionFirstPart);
        break;
      }
      case "deviceReset": {
        bytes.push(0x30);
        break;
      }
      case "setChildLockBehavior": {
        bytes.push(0x35);
        bytes.push(input.data.setChildLockBehavior);
        break;
      }
      case "getChildLockBehavior": {
        bytes.push(0x34);
        break;
      }
      case "setProportionalGain": {
        let kp = Math.round(input.data.setProportionalGain * 131072);
        let kpFirstPart = kp & 0xff;
        let kpSecondPart = (kp >> 8) & 0xff;
        let kpThirdPart = (kp >> 16) & 0xff;
        bytes.push(0x37);
        bytes.push(kpThirdPart);
        bytes.push(kpSecondPart);
        bytes.push(kpFirstPart);
        break;
      }
      case "getProportionalGain": {
        bytes.push(0x36);
        break;
      }
      case "setExternalTemperatureFloat": {
        let temp = input.data.setExternalTemperatureFloat * 10;
        let tempFirstPart = temp & 0xff;
        let tempSecondPart = (temp >> 8) & 0xff;
        bytes.push(0x3c);
        bytes.push(tempSecondPart);
        bytes.push(tempFirstPart);
        break;
      }
      case "setIntegralGain": {
        let ki = Math.round(input.data.setIntegralGain * 131072);

        let kiFirstPart = ki & 0xff;
        let kiSecondPart = (ki >> 8) & 0xff;
        let kiThirdPart = (ki >> 16) & 0xff;
        bytes.push(0x3e);
        bytes.push(kiThirdPart);
        bytes.push(kiSecondPart);
        bytes.push(kiFirstPart);
        break;
      }
      case "getIntegralGain": {
        bytes.push(0x3d);
        break;
      }
      case "setPiRunPeriod": {
        bytes.push(0x41);
        bytes.push(input.data.setPiRunPeriod);
        break;
      }
      case "getPiRunPeriod": {
        bytes.push(0x40);
        break;
      }
      case "setTempHysteresis": {
        let tempHysteresis = input.data.setTempHysteresis * 10;
        bytes.push(0x43);
        bytes.push(tempHysteresis);
        break;
      }
      case "getTempHysteresis": {
        bytes.push(0x42);
        break;
      }
      case "setOpenWindowPrecisely": {
        let enabledValue = input.data.setOpenWindowPrecisely.enabled ? 1 : 0;
        let duration = parseInt(input.data.setOpenWindowPrecisely.duration) / 5;
        let delta = input.data.setOpenWindowPrecisely.delta * 10

        bytes.push(0x45);
        bytes.push(enabledValue);
        bytes.push(duration);
        bytes.push(delta);
        break;
      }
      case "getOpenWindowPrecisely": {
        bytes.push(0x46);
        break;
      }
      case "setForceAttach": {
        bytes.push(0x47);
        bytes.push(input.data.setForceAttach);
        break;
      }
      case "getForceAttach": {
        bytes.push(0x48);
        break;
      }
      case "sendCustomHexCommand": {
        let sendCustomHexCommand = input.data.sendCustomHexCommand;
        for (let i = 0; i < sendCustomHexCommand.length; i += 2) {
          const byte = parseInt(sendCustomHexCommand.substr(i, 2), 16);
          bytes.push(byte);
        }
        break;
      }
      default: {
      }
    }
  }

  return {
    bytes: bytes,
    fPort: 1,
    warnings: [],
    errors: [],
  };
}

function decodeDownlink(input) {
  return {
    data: {
      bytes: input.bytes,
    },
    warnings: [],
    errors: [],
  };
}

// example downlink commands
// {"getOperationalMode":""} --> 0x18
// {"setTargetTemperature":20} --> 0x0E14
// {"setTemperatureRange":{"min":15,"max":21}} --> 0x080F15
// {"setChildLock":true} --> 0701
// {"sendCustomHexCommand":"080F15"} --> 0x080F15
// {"setOpenWindow":{"enabled": true, "closeTime": 20 , "delta": 3, "motorPosition": 540}}  --> 0x0601041C23

// example Node Red mqtt message
// msg.topic = 'v3/<Application ID>@ttn/devices/<End device ID>/down/push'
// msg.payload = {"downlinks":[{f_port:1,decoded_payload:{setTargetTemperature:20},priority:'NORMAL',confirmed:false}]}
