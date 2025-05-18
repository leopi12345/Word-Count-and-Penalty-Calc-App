# Word Count and Penalty Calculator

To run the app in Windows or MacOS, download and run the executable files from Build.

-----------------------------------------------------------------------------------------------------

To run the app in Docker and also to run it on a mobile or tablet (connected to the same wi-fi), follow the intructions below:

Install docker desktop for your OS: https://www.docker.com/products/docker-desktop/

Type cmd in the search box or open terminal on mac

Download tar file from Docker Hub:
https://hub.docker.com/search?q=word_count_and_penalty_calculator

Find the path to the downloaded tar file
Type 'cd mypath' to navigate to the resource
Type:
Docker load -i word_count_and_penalty_calculator.tar

Click on 'images' in docker desktop and click on 'run'
Select port 5000. If you get an error message, repeat and select a different port e.g. 8000

Open cmd and type 'ifconfig' on mac or linux or 'ipconfig /all' on windows. Find the IPv4 private IP address for WI-FI, e.g. 192.168.1.48

Install Flet App on your mobile device or tablet:
From Google Apps: https://play.google.com/store/apps/details?id=com.appveyor.flet&hl=en
From Apps Store https://apps.apple.com/gb/app/flet/id1624979699

Open Flet App on your mobile or tablet
Click on '+'
Type http://'IP address you found earlier':port 
e.g. http://192.168.1.48:5000 
Click on 'add'

Click on the app icon inside the Flet App

-----------------------------------------------------------------------------------------------------

To run the app in Flet, install Python and the requirements (virtual environment is recommended), and run flet:

```
flet run [app_directory]

```

In Linux, the FilePicker control depends on Zenity when running Flet as an app. This is not a requirement when running Flet in a browser.

To install Zenity on Ubuntu/Debian run the following commands:

sudo apt-get install zenity
