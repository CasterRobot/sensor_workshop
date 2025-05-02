import serial
from time import sleep
import sys
import numpy as np
import matplotlib.pyplot as plt


sys.stdout.reconfigure(encoding='utf-8') 


port = '/dev/ttyUSB0'  # or '/dev/ttyACM0'
baud_rate = 921600

#端口接收
serial = serial.Serial(port, 921600, timeout=0.5)
if serial.isOpen():
    print("open success")
else:
    print("open failed")

send_data = bytes.fromhex('A1')
if serial.isOpen():
    serial.write(send_data)
    print("发送成功：", send_data.hex().upper())
    sleep(0.05)

    data_receive = serial.readall()
    if data_receive:
        # 按十六进制打印接收到的数据
        hex_str = ' '.join(f'0x{b:02X}' for b in data_receive)
        # print("接收到数据：", hex_str)
    else:
        print("未收到数据")
    serial.close()
else:
    print("串口未打开")


#获取返回数据
hex_data = hex_str
hex_list = hex_str.strip().split()
byte_data = bytes(int(b, 16) for b in hex_list)
voltage_values = []
for i in range(0, len(byte_data), 2):
    low = byte_data[i]
    high = byte_data[i + 1]
    value = (high << 8) | low  
    voltage_values.append(value)
print(voltage_values)

#电压值转换高度值
indices = indices = list(range(len(voltage_values))) 
min_index = np.argmin (voltage_values)
min_value =voltage_values[min_index]

print(f"激光打到的位置大约是 Pixel Index = {min_index}，电压值 = {min_value}")

height = (min_index * 8 + 8.41  + 3) * 0.001 
print(f"current height is：{height}mm")

#画图
plt.figure(figsize=(14, 6))
plt.plot(indices, voltage_values, color='red', linestyle='-', linewidth=1)

plt.title('Height_Measurement')
plt.xlabel('Pixel Index')
plt.ylabel('Voltage Value')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

plt.show()