# sensor_workshop

conda create -n workshop python=3.10.6


pip install -r requirements.txt

dmesg | grep ttyUSB

sudo chmod 666 /dev/ttyUSB0
sudo chmod 666 /dev/ttyUSB1
