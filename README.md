# CloudDeviceFarmExperiment
Project to create cloud device farm for mobile automation testing purpose.

### Prerequisite
1. If you are not using real IOS devices then you need Macintosh environment to run IOS emulator
2. Python installed
3. Android studio for Android emulator
4. Xcode for IOS emulator

### Introduction

The idea of this project is to create a cloud device farm which is pretty similar to 3rd party services like Browserstack, Sauce Lab, etc.
By using your own cloud device farm this might save you alot of money per year, which you could use the money to buy real devices for your project's assets. Browserstack's price varies from $999 to $4979 per month for non enterprise plan.

Below is project's flow to give it a better picture about what we are going to do.

![flow](https://user-images.githubusercontent.com/21231342/198958311-0f5e2682-05ad-4b34-9b2e-9343926082ff.jpg)

### Create Android device management tables in MySQL

> <sub>CREATE TABLE `device_list_android` (
  `device_name` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `device_status` int(5) DEFAULT NULL,
  `os_version` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `port` int(6) DEFAULT NULL
)</sub>

<img width="204" alt="Screen Shot 2022-10-31 at 15 04 22" src="https://user-images.githubusercontent.com/21231342/198960529-92f798dc-ccbe-4e1c-b27a-3dc1c9bece47.png">


### Create IOS device management tables in MySQL

> <sub>CREATE TABLE `device_list_ios` (
>  `device_name` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
>  `device_status` int(5) DEFAULT NULL,
>  `os_version` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
>  `device_id` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL
> )</sub>

<img width="207" alt="Screen Shot 2022-10-31 at 15 06 48" src="https://user-images.githubusercontent.com/21231342/198960900-d51bf56e-135b-41e3-ba56-79ea20042562.png">

### Clone project
How to install Python >> https://www.python.org/downloads/

Create Python virtual environment
> python3 -m venv /path/to/new/virtual/environment

Clone this repo to your PC/Laptop/Server
> git clone

Install requirements.txt
> pip install -r requirements.txt

Run server
> python3 manage.py runserver

## Using Android emulator
### Create several Android devices on Android Studio

<img width="1433" alt="Screen Shot 2022-10-31 at 15 23 04" src="https://user-images.githubusercontent.com/21231342/198963700-10c79307-1eac-4898-b61a-0b17498e84a6.png">

Insert each device details into table device_list_android

<img width="499" alt="Screen Shot 2022-10-31 at 15 25 33" src="https://user-images.githubusercontent.com/21231342/198964264-9b6cb885-32df-4566-81cc-00954116a3f1.png">

### Register list of IOS emulators to table device_list_ios

1. Open terminal
2. Run xcrun simctl list
3. Under == Devices == choose IOS version and device
4. Insert IOS device details into table device_list_ios (get device_id from step 3)

<img width="566" alt="Screen Shot 2022-10-31 at 15 49 27" src="https://user-images.githubusercontent.com/21231342/198968798-897ec827-fd9d-4ee6-a4c2-5e335ee51f25.png">

<img width="703" alt="Screen Shot 2022-10-31 at 16 15 56" src="https://user-images.githubusercontent.com/21231342/198973498-6c6827fa-4e9a-4eb2-a148-212f637c96ad.png">

## Django setup
### Adjust settings.py in Django project

1. Adjust database connections in settings.py
2. If you are not using Mac, adjust code in function start_device_android in views.py (see pic below)

<img width="816" alt="Screen Shot 2022-10-31 at 17 59 33" src="https://user-images.githubusercontent.com/21231342/199164887-9054f3e1-d7e5-41b7-a4ce-f69cf0c9e136.png">

3. If you are deploying to server, adjust url in function create_appium_hub in views.py (see pic below)

<img width="622" alt="Screen Shot 2022-10-31 at 17 32 02" src="https://user-images.githubusercontent.com/21231342/199164902-85e06395-5b6b-4c3e-b24a-8abcc4e188b0.png">

## Usage
1. Hit endpoint to start Android/IOS device
2. Use datas from JSON response in Appium desired capabilities
3. Hit endpoint to start Appium server
4. You will get JSON response of Appium hub url, use that to create Appium connection
5. In teardown process do this:
- Hit endpoint to stop Android/IOS device
- driver.quit in your code

## Error code mapping
0: Success
1: Fail
2: Run out of devices
3: Missing query param

## Discussion
1. Is using real device is better than using emulator?
- Not really, the emulator is invented to simulate the real device. Also, if your automation test is not specifically need to be run on certain device type, so it would be a cost saving to just use emulator.

2. How much RAM and space needed to run this device farm?
- Depends on how many emulators you need to run at once. Using real device will save alot of RAM usage.

3. Do you have dummy apps to test?
- Yes, you can check in folder dummy_apps
