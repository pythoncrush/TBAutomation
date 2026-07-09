import pytest
import logging
import pandas as pd
from tb_auto_base import TBAUTO
from tb_auto_utilities import HUB_SIZE
import pdb
import re

logging.basicConfig()

class TestDevices():
    tb_instance = TBAUTO()
    port = '1-' + HUB_SIZE
    adb_serial_list = []
    ios_serial_list = []
    df = pd.DataFrame()

    @pytest.fixture
    def setup_and_teardown_resources(self):
        logging.debug("start setup")
        
        logging.debug(f"Turning on all ports on hub")        
        port = '1-' + HUB_SIZE
        self.tb_instance.usb_hub_command(action='on',port=self.port)

        self.tb_instance.discover_devices_on_usb_bus()
        self.df = self.tb_instance.write_usb_info_to_dataframe()
        #self.df = self.tb_instance.df
        
        #converting to strings
        self.df = self.df.astype(str)
        
        #printing dataframe to make sure it loooks good
        logging.debug(f"data frame is \n {self.df}")
        
        yield

        logging.debug("start teardown")
        logging.debug(f"Turning off all ports on hub")        

        self.tb_instance.usb_hub_command(action='off',port=self.port) 

    @pytest.mark.samsung
    @pytest.mark.sanity
    def test_application_size(self):
        logging.debug("calculating size of applications started")
        app_size = self.tb_instance.calculate_size_of_file(path_to_file='com.turtlebeach.swarm2-Signed.apk')
        assert app_size > 41310862

    @pytest.mark.mobile_app_installation
    def test_application_on_samsung(self,setup_and_teardown_resources):
        logging.debug("application install of Samsung started")
        
        #Samsung case
        df_samsung = self.df.loc[self.df["usb_product_name"].str.startswith('Samsung', na=False)]
        samsung_serial = df_samsung['serial']
        samsung_serial = samsung_serial.to_string(index=False)
        if samsung_serial:
            self.adb_serial_list.append(samsung_serial)

        #Enable Bluetooth status for samsung mobile
        self.tb_instance.send_adb_command(serial=self.adb_serial_list[0], command_string = 'cmd bluetooth_manager enable')
        
        app_status = self.tb_instance.uninstall_mobile_app_android(serial_list=self.adb_serial_list[0])
        if app_status:
            print(f'app uninstall status is {app_status}')
            app_status = self.tb_instance.install_mobile_app_android(serial_list=self.adb_serial_list[0])
            print(f'app install status is {app_status}')
            assert app_status

    @pytest.mark.ios
    @pytest.mark.sanity
    def test_application_size(self):
        logging.debug("calculating size of applications started")
        app_size = self.tb_instance.calculate_size_of_file(path_to_file='Swarm2.App.TB.ipa')
        assert app_size < 41025683

    @pytest.mark.ios
    @pytest.mark.mobile_app_installation
    def test_application_on_ios(self,setup_and_teardown_resources):
        logging.debug("application install of iOS app started")
        
        #iOS case
        df_ios = self.df.loc[self.df["usb_product_name"].str.startswith('Apple', na=False)]
        ios_serial = df_ios['serial']
        ios_serial = ios_serial.to_string(index=False)
        if ios_serial:
            self.ios_serial_list.append(ios_serial)

            
        #TODO Enable Bluetooth for iOS devices
        #self.tb_instance.send_adb_command(serial=self.ios_serial_list[0], command_string = 'cmd bluetooth_manager enable')
        
        app_status = self.tb_instance.install_audio_hub_app_ios(name_of_application='Swarm2.App.TB.ipa')
        print(f'app install status is {app_status}')
        assert app_status