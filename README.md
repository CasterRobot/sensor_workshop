# sensor_workshop

## 下载

1. 下载此程序，解压到你想要的文件夹，记住此程序的路径是在`D:`，`C:`, 还是`E:`
   
2. 搜索cmd，命令提示符，右键以管理员身份运行

3. 输入你程序所在的硬盘路径，例如：
   
      `D:`
  
      然后回车
  
4. 然后输入
   
      `cd D:/blablabla/sensor_workshop-main/`
  
      回车
  
      将`D:/blablabla/sensor_workshop-main/`改成你的程序的路径。

## 安装你的python运行环境（这一步大家已经做完，可以略过）

1. 新建一个新的虚拟环境
   
      `conda create -n workshop python=3.10.6`
  
      然后回车
  
2. 激活该环境

      `conda activate workshop`
   
      然后回车
   
4. 安装需要的安装包
   
      `pip install -r requirements.txt`
  
      然后回车

5. 可选： 单独下载一个安装包

      `pip install pyserial`
  
      回车

      `pip install numpy`
  
      回车

      ......

## 运行你的程序

1. 激活虚拟环境

      `conda activate workshop`
  
      然后回车

2. 运行程序

      `python main.py`
   
      回车

## 使用该界面

1. 点击 `connect`
2. 选择 `num of points`
3. 点击 `measure`
4. 选择 `num of points`
5. 点击 `measure`
6. 重复测量十次，

## 注意事项

1. 测量只能一个一个来，不能测量第一行，接着测量第三行.
2. `dispaly or not`可以帮你选中是否显示本次测量。



以下忽略，用于linux系统


dmesg | grep ttyUSB

sudo chmod 666 /dev/ttyUSB0
sudo chmod 666 /dev/ttyUSB1
