import requests
import binascii
import datetime
import pytz

time_zone = pytz.timezone("America/New_York")

api_key = 'NNSXS.OK22X5UNWI64GN3CIWOKCT7VZUEGN63BVKB4UDQ.SXLPBCEX3AVUUXK2WWBEVSLKZQ7XOSLV7HEYCFBSLREQRAL2LUKA'
base = 'https://tutorial123.nam1.cloud.thethings.industries/api/v3'

def downlink(frm_payload):  
  
  headers = {
  'Authorization': f'Bearer {api_key}',
  'Content-Type': 'application/json' 
  }

  data = {
    "downlinks":[{
      "frm_payload":frm_payload,
      "confirmed":True,
      "f_port":1}]
  }


  payload = requests.post(f'{base}/as/applications/temp-sensor/devices/ai-image/down/push', json=data,  headers=headers)

  if payload.status_code != 200:
    print(f"Error: {payload.status_code}")
    print(f"Payload not successfully downlinked at {datetime.datetime.now()}")
    exit()

def get_uplinks(num):
  current_time = datetime.datetime.now(time_zone)
  earlier_time = current_time - datetime.timedelta(minutes=10)
  formatted_time = earlier_time.strftime('%Y-%m-%dT%H:%M:%SZ')

  headers = {
  'Authorization': f'Bearer {api_key}',
  }

  params = {
    'limit': num,  
    'after': formatted_time
}

  payload = requests.get(f'{base}/as/applications/temp-sensor/devices/ai-image/packages/storage/uplink_message', headers=headers, params=params)

  if payload.status_code != 200:
    print(f"Error: {payload.status_code}")
    print(payload.reason)
    print(f"Uplink not successfully retrived at {datetime.datetime.now()}")
    exit()
  else:
    return payload.content

def toBase64(hex):
    binary = binascii.a2b_hex(hex)
    base64 = str(binascii.b2a_base64(binary))
    base64 = base64[2:len(base64)-3] 
    return base64

def toHex(base64):
    binary = binascii.a2b_base64(base64)
    hex = str(binascii.b2a_hex(binary))
    hex = hex[2:len(hex)-1] 
    return hex

