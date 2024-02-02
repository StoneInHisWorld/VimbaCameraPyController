import os
import queue
import threading
import time

from tqdm import tqdm

import picshow
from VimbaPython.Source.vimba import PixelFormat
from camera import Camera

"""设置相机参数"""
gain = 23
exposTime = 300000

"""设置图片展示参数"""
dataset_path = './data'
fruit_root = './fruits'
path_iter = os.walk(dataset_path)
_, _, files = next(path_iter)


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
        # TODO:对帧图片进行预处理

        # 通知队列该帧已处理完毕
        pending_pics.task_done()
    except Exception:
        # 针对重复拍照的帧，不做任何事
        pass
    # 通知相机此帧已处理完毕
    cam.queue_frame(frame)


if __name__ == '__main__':
    end_signal = threading.Event()
    pending_pics = queue.Queue()

    # TODO:初始化相机
    camera = Camera(0)
    camera.set_exposTime(exposTime)
    camera.set_gain(gain)

    # 获取屏幕尺寸并设置好plt属性
    screen_size = picshow.get_screen_size()
    print(screen_size)
    picshow.prepare_plt(screen_size=screen_size, win_size=(770, 960))

    t2 = threading.Thread(
        target=camera.AS_shoot,
        args=(frame_handler, end_signal)
    )
    t2.start()
    # TODO: 设置初始等待时间
    # 在此时间内可以将matplotlib窗口全屏化
    sleep = 5
    for wait in range(3, 0, -1):
        print(f'\r实验将在{wait}秒后开始，请做好准备！', flush=True, end='')
        time.sleep(1)

    # 图片展示循环，需要在main_thread中
    with tqdm(files, desc='\r解包文件……', unit='类', mininterval=1, position=0, leave=True) as pbar:
        # 对每一个npy文件进行循环
        for np_file in pbar:
            # TODO: 整理存储目录
            fruit_dir = os.path.join(fruit_root, np_file.split('.')[0])
            label_dir = os.path.join('./labels/', np_file.split('.')[0])
            if not os.path.exists(fruit_dir):
                os.mkdir(fruit_dir)
            if not os.path.exists(label_dir):
                os.mkdir(label_dir)
            # TODO:进行图片读取
            imgs = None
            # TODO:进行图片展示
            for i, img in enumerate(tqdm(
                    imgs, desc=f'\r解包{np_file}……', unit='张',
                    mininterval=1, position=0, leave=True
            )):
                # TODO:对获取的图片进行预处理
                pic = None
                # 展示图片
                picshow.show_pic(pic, sleep=sleep)
                # 等待图片加载完毕
                time.sleep(sleep)
                # 将图片保存路径放在路径中，同时通知拍照
                pending_pics.put_nowait(
                    os.path.join(fruit_dir, str(i) + '.jpg')
                )
                # TODO: 设置拍照间隔
                sleep = 0.25
    end_signal.set()
