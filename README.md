"# TBAUTOMATION" 
Please run this on mac, windows sucks for software development.
Try to do everything from the command line terminal on mac.
1. Install Warp window manager, amazing
2. Install a text editor (VSCode, Sublime, Notepad++, Pycharm)
3. Use a high quality hub that shows up when you type lsusb in the terminal
4. Install ruby on your mac
5. Install idevicesyslog (This is for logging iPhone debug messages)
	ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

	brew install -v --devel --fresh automake autoconf libtool wget libimobiledevice

	brew install -v --HEAD --fresh --build-from-source ideviceinstaller

Set up git on your mac or windows machine. generate an SSH key and add it to your github profile to establish trust

We will eventually have to install a lot more software on mac. Like XCode, xcuitests so you can install that if you want also
https://www.lambdatest.com/xcuitest
http://appium.io/docs/en/2.1/quickstart/install/

We will need to get the udids on iphones as well.
https://stackoverflow.com/questions/56423608/where-to-find-iphone-device-udid-if-itunes-expected-to-be-retired-by-macos-10-1


Pre-requsites:
1. Make sure you enable developer mode on Android devices, then enabled USB debugging so they can be authorized on the host
2.Install Python3	
	https://www.python.org/downloads/macos/
3. Install adb 
	 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
	  brew install android-platform-tools
	  adb devices
4. Install pylint
	brew install pylint
5. Install pip
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	python3 get-pip.py


Environment setup
1. Verify version with this command python3 -v
2. Make a directory where you store virtual environments for testing 
	cd ~
	mkdir venvs
	cd venvs
	python3 -m venv automation_dev1
3. It's important to name them well activate them to keep versions sane
4. Activate the virtual environment created in step 2.
	source ~/venvs/automation_dev1/bin/activate
5. Now clone the repo and work from there, anytime a change is necessary add me as code reviewer and I'll provide feedback.
git clone git@github.com:Turtle-Beach-Corporation/TBAUTOMATION.git
now install requirements
pip install -r requirements.txt
6. add adb to your bash path. Make sure you are running in bash shell echo $0, if it says ksh or something else type bash, you are now in bash
7. Navigate to https://developer.android.com/studio/releases/platform-tools.html and click on the SDK Platform-Tools for Mac link.
8. cd ~/Downloads/
9. unzip platform-tools-latest*.zip 
10. mkdir ~/.android-sdk-macosx
11. mv platform-tools/ ~/.android-sdk-macosx/platform-tools
12. echo 'export PATH=$PATH:~/.android-sdk-macosx/platform-tools/' >> ~/.bash_profile
13. source ~/.bash_profile
14. make sure your phones and TB HW are connected and showing up in lsusb on terminal
	python3 tb_auto_base.py
 return   
