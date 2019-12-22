import time
from bluezero import microbit
from keyboardRead import NonBlockingConsole

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
                # Define microbit object
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

                # Connect to microbit
                print ("....Connecting")
                devices[key].connect()
                print ("....Connected")
            except:
                # If initilisation or connection failed remove this device from device list
                print ("....Initialisation or Connection failed")
                devices.pop(key, None)

            line=fp.readline()
except:
    print("Failed to open config file")
    exit()

# Check that at least one device is connected to - if not exit
if (devices is None or len(devices)==0):
    print ("No connected devices - exiting")
    exit()

# Loop whilst listening for keyboard input (on the Pi)
with NonBlockingConsole() as nbc:
    looping = True
    while looping:

        # Check each device in turn - getting the unique key of each device
        for dKey in devices:
            
            # If the escape key is pressed on the PI then break
            keyboardVal = nbc.get_data()
            if keyboardVal == '\x1b':  # x1b is ESC
                print ("Raspberry Pi Escape key pressed")
                looping=False
            elif keyboardVal == 'm':  
                msg = input("Enter message to output to all Pis:")
                for d in devices:
                    devices[d].text=msg


            # If the A button is pressed - exit the loop (a kill switch)
            if (devices[dKey].button_a > 0):
                print("Device [", dKey, "] Button A Pressed" )
                looping=False
            
            # Print the temperature from the device 
            print('Temperature [', dKey, '] = ', devices[dKey].temperature)
        
        time.sleep(1)


# Tidy up by disconnecting from all devices
print ("Disconnecting from all devices")
for dKey in devices:
    print ("..Device [",dKey,"]")
    print ("....Disconnecting")
    devices[key].disconnect()
    print ("....Disconnected")