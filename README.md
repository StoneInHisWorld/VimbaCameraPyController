# VIMBA CAMERA Controller v1.0
对于支持vimba接口的相机控制器进行基本功能的封装

## 使用之前
需要在[Allied Vision™官方网站](https://www.alliedvision.cn/cn/products/software/vimba-sdk/)中下载SDK，放在与本文件的同级目录

## VimbaCamera
Vimba相机对象，封装了相机（vimba接口）提供的基础功能。
可以通过set方法设置相机的参数，将会在获取下一帧之前（处理下一帧之前）更新相机参数。  

## 使用范例
```python
from vbcamera import VimbaCamera as Camera
import cv2
import threading
from threading import Event

def frame_handler(cam, frame):
    """帧处理器，将vimba接口传入的相机对象和帧对象进行处理
    
    请注意：接口不可更改！
    :param cam: 正在拍照的相机对象
    :param frame: 帧对象
    :return: None
    """
    # 将图片转换成黑白
    frame.convert_pixel_format(PixelFormat.Mono8)
    img = frame.as_opencv_image()
    # 保存图片
    cv2.imwrite('./', img)
    # 通知相机此帧已处理完毕
    cam.queue_frame(frame)

# 开启相机
camera = Camera(0, expos_time=1000, gain=0)
# 同步拍摄
for frame in camera.syn_shoot():
    cv2.imwrite('./', frame)
    if input('1：继续/ 0：结束') == '0':
        break
del camera
        

# 异步拍摄
camera = Camera(0, expos_time=1000, gain=0)
# 所有设备同步开启的信号
start_signal = Event()
end_signal = Event()
cam_thread = threading.Thread(
    target=camera.asyn_shoot,
    args=(start_signal, end_signal, frame_handler)
)
cam_thread.start()
start_signal.set()
"""过了一段时间"""
end_signal.set()
del camera
```




