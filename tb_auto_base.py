'''
        This is the base class for the TBAUTOMATION project written in a object oriented style
        This class can be instatiated and re-purposed for other automation
        functions in other modules
'''
import sys
import re
import subprocess
import pandas as pd
import pytest
import pixelmatch
import time
import os


class TBAUTO():
    '''
    Base Class for TBAUTO, class members are obtained from usb bus
    '''
    def __init__(self):
        '''
        Base Class for TBAUTO, class members are obtained from usb bus
        '''
        self.vid = []               #Setting vid list class member to empty
        self.pid = []               #Setting pid list class member to empty
        self.serial = []            #Setting serial list class member to empty
        self.usb_product_name = []  #Setting USB product name list class member to empty
        self.df = None              #Setting data frame (df) class member to empty
        self.output = None          #response output of adb shell command execution
        self.port = None            #port number on USB hub (used for uhubctl_wrapper)
        self.hostname = None        #hostname (will be used for test runner)

    def discover_devices_on_usb_bus(self):
        '''
        This function using lsusb to scan the usb bus for devices
        '''
        if sys.platform in {'darwin','linux','linux2'}:
            command_to_execute = ['lsusb']
            lsusb_output = subprocess.check_output(command_to_execute).decode('utf-8')
            for line in lsusb_output.splitlines():
                if 'Bus' in line:
                    usb_match = re.search(r'Bus\s\S{3}\sDevice\s\S{3}:\sID\s(\S{4}):(\S{4})\s(.*)\s{2}Serial:\s(.*)',line)
                    if usb_match:
                        self.vid.append(usb_match.group(1))
                        self.pid.append(usb_match.group(2))
                        #The replace functions are to sanitize the data for name, removed commas, spaces and dots so no
                        #weird stuff happens when we start accesing this database for auomation
                        self.usb_product_name.append(usb_match.group(3).replace(",", "").replace(" ", "_").replace(".", ""))
                        self.serial.append(usb_match.group(4))
        elif sys.platform in 'win32':
            #windows usb logic goes here:
            print('hi windows')
        else:
            print('sorry bro, platform not supported')

    def write_usb_info_to_dataframe(self):
        '''
        This function takes the discovered information discovered and writes it into 
        a dataframe, this is a database that we can access and an excellent
        data structure for high cardinality

        sample data
           vid   pid                  serial                         usb_product_name        port
        0  2109  0822                 000000001                      VIA_Labs_Inc_USB31_Hub  nan
        1  10f5  2199              6302FFFF9402                       10f5_Stealth_Pro_Xbox    4
        2  04e8  6860          299ae744a31c7ece  Samsung_Electronics_Co_Ltd_SAMSUNG_Android    3
        3  05ac  12a8  000081010006799C3400801E                            Apple_Inc_iPhone    2
        4  10f5  2197              8802FFFF2502               10f5_Stealth_Pro_Xbox_Headset    1

        '''
        column_headers = ['vid', 'pid', 'serial', 'usb_product_name', 'port']
        
        # initialize data composed of list of lists
        data = {'vid': self.vid,
                'pid': self.pid,
                'serial': self.serial,
                'usb_product_name': self.usb_product_name,
                'port': self.port}

        # Create the pandas DataFrame
        self.df = pd.DataFrame(data, columns=column_headers)

        #pulling in the hub to get correct port inserted
        hub_stdout = self._uhubctl_wrapper()
        lines = hub_stdout.splitlines()
        for line in lines:
            #add parser for these kinds of lines here
            #Current status for hub 20-2.4.3 [2109:2822 VIA Labs, Inc. USB2.0 Hub, USB 2.10, 4 ports, ppps]
            if 'Port' in line:
                matched_line = re.search(r"\s+Port\s(\d):\s\d+\spower\s(enable|highspeed enable)\sconnect\s\[(\S{4}):(\S{4})",line)
                if matched_line:
                    port = matched_line.group(1)
                    vid_parsed = matched_line.group(3)
                    pid_parsed = matched_line.group(4)
                    self.df.loc[(self.df['vid'] == vid_parsed) & (self.df['pid'] == pid_parsed), 'port'] = port
            continue
        return self.df

    def find_devices_on_adb(self):
        return (device_serial_list := [line.decode('utf-8') for line in subprocess.check_output("adb devices").split() if len(line) >= 10])

    def uninstall_mobile_app_android(self, serial_list):
        #device_serial_list = self.find_devices_on_adb(self)
        for serial in serial_list:
            cmd = 'adb -s ' + serial + ' shell pm uninstall -k --user 0 com.turtlebeach.swarm2-Signed'
            subprocess.call(cmd, shell=True)
        return True

    # def uninstall_roccat_app(self):
    #     device_serial_list = self.find_devices_on_adb(self)
    #     for device in device_serial_list:
    #         cmd = 'adb -s ' + device + ' shell pm uninstall -k --user 0 com.turtlebeach.roccat1'
    #         subprocess.call(cmd, shell=True)
    #     return True

    def install_mobile_app_android(self, serial_list):
        #serial_list = self.find_devices_on_adb(self)
        for serial in serial_list:
            cmd = 'adb -s ' + serial + ' install com.turtlebeach.swarm2-Signed.apk'
            subprocess.call(cmd, shell=True)
        return True

    def install_mobile_app_ios(self, name_of_application):
        cmd = 'ipa-deploy ' + name_of_application
        subprocess.call(cmd, shell=True)
        return True


    # def install_roccat_app(self):
    #     device_serial_list = self.find_devices_on_adb(self)
    #     for device in device_serial_list:
    #         cmd = 'adb -s ' + device + ' install com.turtlebeach.roccat1.apk'
    #         subprocess.call(cmd, shell=True)
    #     return True

    def _uhubctl_wrapper(self):
        #internal class function
        output = subprocess.check_output('uhubctl', shell=True)
        return output.decode('utf-8')

    def usb_hub_command(self, action, port):
        '''
        This function will allow us to hook up N numbers of USB devices and isolate specific 
        ones to be used in testing, by turning on the devices we want on
        -a is action the valid actions are:
            on
            off
            cycle
            toggle
        -p is the port number (this can be found by typing uhubctl on the terminal)
        '''
        print(f"*************************Turning port {port} {action} *************************")

        output = subprocess.check_output('uhubctl -a ' + action + ' -p ' + port, shell=True)
        time.sleep(5)
        return output

    def send_adb_command(self,serial,command_string):
        '''
        This function will allows us to send any adb command to a device on adb 
        '''
        adb_command_to_execute = 'adb ' + '-s ' + serial + ' shell ' + command_string
        output = subprocess.check_output(adb_command_to_execute, shell=True)
        return output.decode('utf-8')

    def calculate_size_of_file(self,path_to_file):
        '''
        This function calculates the size of a file and returns to size in  
        '''
        return os.path.getsize(path_to_file)

if __name__ == "__main__":
    my_class_instance = TBAUTO()
    my_class_instance.discover_devices_on_usb_bus()
    my_class_instance.write_usb_info_to_dataframe()
    #this is done to shorten list comprehension below
    df = my_class_instance.df
    adb_serial_list = []
    ios_serial_list = []

    #converting to strings
    df = df.astype(str)
    #printing dataframe to make sure it loooks good
    print(df)
    #my_class_instance.uhubctl_wrapper()
    #Samsung case
    # df_samsung = df.loc[df["usb_product_name"].str.startswith('Samsung', na=False)]
    # samsung_serial = df_samsung['serial']
    # samsung_serial = samsung_serial.to_string(index=False)
    # if samsung_serial:
    #     adb_serial_list.append(samsung_serial)

    #Pixel case
    # df_google = df.loc[df["usb_product_name"].str.startswith('Google', na=False)]
    # google_serial = df_google['serial']
    # google_serial = google_serial.to_string(index=False)
    # adb_serial_list.append(google_serial)

    # #Apple case
    # df_apple = df.loc[df["usb_product_name"].str.startswith('Apple', na=False)]
    # ios_serial = df_apple['serial']
    # ios_serial = ios_serial.to_string(index=False)
    # ios_serial_list.append(ios_serial)

    # app_status = my_class_instance.uninstall_audio_hub_app(serial_list=adb_serial_list)
    # if app_status:
    #     print(f'app uninstall status is {app_status}')
    #     app_status = my_class_instance.install_audio_hub_app(serial_list=adb_serial_list)
    #     print(f'app install status is {app_status}')
    
    # #For Android we can use adb command module already written
    # #iOS will be done with appium/safari or using vysor and the usb BT dongle

    # #Enable Bluetooth status for Google
    # my_class_instance.send_adb_command(serial=google_serial, command_string = 'cmd bluetooth_manager enable')
    # print('sleeping for 5 seconds after turning on Bluetooth')
    # time.sleep(5)

    # #TODO add appium or the vysor automation stuff here
    # #We can take screenshots using the vysor CLI
    # #Then we use pixel match to compared against graphoc files
    # #we get from Karen

    # #Turn off Bluetooth, put device in low power mode, and reboot, this is most neutral state for the phone
    # my_class_instance.send_adb_command(serial=google_serial, command_string = 'cmd bluetooth_manager disable')
    # my_class_instance.send_adb_command(serial=google_serial, command_string = 'settings put global airplane_mode_on 1 ')
    # #my_class_instance.send_adb_command(serial=google_serial, command_string = 'reboot')
