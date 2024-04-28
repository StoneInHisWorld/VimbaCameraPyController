import os
import queue
import threading
import time

import cv2
from tqdm import tqdm

import picshow
from VimbaPython.Source.vimba import PixelFormat
from camera import Camera

# TODO:设置数据读取目录以及产出目录
dataset_root = './data/'
fruit_root = './fruits/{}'.format(time.strftime('%Y-%m-%d-%H.%M', time.localtime()))
path_iter = os.walk(dataset_root)
_, _, files = next(path_iter)

# 设置相机参数
gain = 0
exposTime = 50

# TODO: 设置图片展示参数


def frame_handler(cam, frame):
    """
    帧处理器，将vimba接口传入的相机对象和帧对象进行处理。注意：接口不可更改！
    :param cam: 正在拍照的相机对象
    :param frame: 帧对象
    :return: None
    """
    # 如果更改了图片则保存此帧，否则不做任何事
    try:
        pic_path = pending_pics.get_nowait()
        frame.convert_pixel_format(PixelFormat.Mono8)
        img = frame.as_opencv_image()
        # TODO: 对帧图片进行预处理

        # 保存图片
        cv2.imwrite(os.path.join(pic_path), img)
        pending_pics.task_done()
    except Exception as e:
        print(e)
        pass
    # 通知相机此帧已处理完毕
    cam.queue_frame(frame)


if __name__ == '__main__':
    # 设置线程通信信号
    change = threading.Event()
    end_signal = threading.Event()
    pending_pics = queue.Queue()

    # 获取相机对象
    camera = Camera(0, expos_time=exposTime, gain=gain)

    # 获取屏幕尺寸并设置好plt属性
    screen_size = picshow.get_screen_size()
    print(f"屏幕大小为{screen_size}")
    picshow.prepare_plt(screen_size=screen_size, win_size=(770, 960), figsize=(5, 5))
    # 开启相机
    camera.AS_shoot(end_signal, frame_handler)
    # 设置初始等待时间，在此时间内可以将matplotlib窗口全屏化
    sleep = 5
    # 实验开始提示
    for wait in range(3, 0, -1):
        print(f'\r实验将在{wait}秒后开始，请做好准备！', flush=True, end='')
        time.sleep(1)

    # 图片展示循环，需要在main_thread中
    with tqdm(files, desc='\r解包文件……', unit='类', mininterval=1, position=0,
              leave=True) as pbar:
        for i, img in enumerate(pbar):
            # TODO: 对读取的图片进行预处理
            pic = img
            # 展示图片
            picshow.show_pic(pic, sleep=sleep)
            # 等待图片加载完毕
            time.sleep(sleep)
            # 将图片保存路径放在路径中，同时通知拍照
            # TODO: 生成图片保存路径
            path = f"{str(i)}.jpg"
            pending_pics.put_nowait(path)
            sleep = 0.25
    end_signal.set()
