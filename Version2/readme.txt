#Update and upgrade rasp
sudo apt-get update && sudo apt-get upgrade

#Check your python version
python3 -V

#Install pip and virtualenv
sudo apt-get install python3-pip python3-virtualenv
mkdir smartcar
cd smartcar

#Install virtual environemnt
python3 -m pip install virtualenv
python3 -m virtualenv env

#Activate the virtual env
source env/bin/activate

#Install nessary packages
sudo apt install -y build-essential cmake pkg-config libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 libqt5gui5 libqt5webkit5 libqt5test5 python3-pyqt5 python3-dev

#Install OpenCV
pip install opencv-contrib-python

#Testing
python
import cv2
cv2.__version__

#Deactivate env
deactivate


#### Run the script ###
cd Desktop
cd smartcar
source env/bin/activate # run python script with virtual env
python Main.py




