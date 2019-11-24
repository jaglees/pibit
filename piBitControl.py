import time
from bluezero import microbit

devices={}
filepath = './microbits.cnf'
print ("Initialising microbits found in ", filepath)
try: 

    # Read list of Microbit MAC addresses and attempt to connect to each
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            key=line.strip()
            print ("..Device: [",key.strip(),"]")
            try:
                print ("....Initialising")
                devices[key] = microbit.Microbit(adapter_addr='B8:27:EB:66:CC:EF',
                                    device_addr=key,
                                    accelerometer_service=True,
                                    button_service=True,
                                    led_service=True,
                                    magnetometer_service=False,
                                    pin_service=False,
                                    temperature_service=True)
                print ("....Initialised")

                print ("....Conneting")
                devices[key].connect()
                print ("....Connected")
            except:
                print ("....Initialisation or Connection failed")
                devices.pop(key, None)

            line=fp.readline()
except:
    print("Failed to open config file")
    exit()

# Check that at least one device is connected to - if not exit
if (devices is None or len(devices)==0):
    print ("Connection to all devices failed - exiting")
    exit()

looping = True
while looping:

    # Check each device in turn
    for key in devices:
        
        # If the A button is pressed - exit the loop (a kill switch)
        if (devices[key].button_a > 0):
            print("Device [", key, "] Button A Pressed" )
            looping=False
        
        # Print the temperature from the device 
        print('Temperature [', key, '] = ', devices[key].temperature)
    
    time.sleep(1)

# Tidy up by disconnecting from all devices
print ("Disconnecting from all devices")
for key in devices:
    print ("..Device [",key,"]")
    print ("....Disconnecting")
    devices[key].disconnect()
    print ("....Disconnected")