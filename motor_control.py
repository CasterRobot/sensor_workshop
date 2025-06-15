import serial
import time
import sys
import matplotlib.pyplot as plt
import numpy as np


class motor:
    def __init__(self, port = '/dev/ttyUSB0', baud_rate = 115200):

        self.ser = serial.Serial(port, baud_rate, timeout=0.5)

        if self.ser.isOpen():
            print("open success")
        else:
            print("open failed")

    def move_to(self, angle):
        """
        angle: 0-360
        """
        hex_bytes = int(3200 * angle / 360).to_bytes(2, byteorder='big', signed=False)
        send_data = bytes.fromhex('A1' + hex_bytes.hex().upper())
        self.ser.write(send_data)
        print("发送成功：", send_data.hex().upper())
        time.sleep(3)

    def disconnect(self):
        self.ser.close()

class laser:

    def __init__(self, port = '/dev/ttyUSB1', baud_rate = 9600):

        self.ser = serial.Serial(port, baud_rate, timeout=0.5)

        if self.ser.isOpen():
            print("open success")
        else:
            print("open failed")

    def get_distance(self):
        # send_data = bytes.fromhex('A1')
        dis = 0

        send_data = 'iSM'
        self.ser.write(send_data.encode('utf-8'))

        data_receive = self.ser.readall()
        if data_receive:
            # 按十六进制打印接收到的数据
            dis = data_receive.decode('utf-8').strip().split("=")[-1].split("m")[0]
            dis = float(dis)
            # print("接收到数据：", hex_str)
        else:
            print("未收到数据")
            dis = None
        
        time.sleep(1)

        return dis

    def disconnect(self):
        self.ser.close()

if __name__ == "__main__":

    motor_ins = motor(port = '/dev/ttyUSB1', baud_rate = 115200)
    laser_ins = laser(port = '/dev/ttyUSB0', baud_rate = 9600)

    for i in range(0, 361, 90):
        motor_ins.move_to(i)
        print(laser_ins.get_distance())

    motor_ins.disconnect()
    laser_ins.disconnect()
    # data_receive = ser.readall()
    # # 按十六进制打印接收到的数据
    # print(data_receive)
    # hex_str = ' '.join(f'0x{b:02X}' for b in data_receive)