import os
import threading
import time

import cv2
from tqdm import tqdm

import camera as camera
import picshow

# 打开数据库中的图片并进行显示
from VimbaPython.Source.vimba import PixelFormat

dataset_dir = './data/MNIST'
fruit_dir = './fruits/{}'.format(time.strftime('%Y-%m-%d-%H.%M', time.localtime()))
exposure_time = 70
gain = 1
px_format = PixelFormat.Mono8

print('请准备好进行数据采集...')
time.sleep(10)


def picshowting_thread(change_signal):
    # 获取屏幕尺寸并设置好plt属性
    screen_size = picshow.get_screen_size()
    print(screen_size)
    picshow.prepare_plt(screen_size=screen_size, win_size=(770, 960))

    # 流水线
    file_names = picshow.get_pic_names(dataset_dir)
    with tqdm(file_names, desc='打开图片...', unit='img', position=0, leave=True) as pbar:
        for fn in pbar:
            # 显示
            pbar.set_description(f'处理{fn}')
            path = os.path.join(dataset_dir, fn)
            picshow.show_pic(path, sleep=0.01)

            # 通知拍照
            change_signal.set()
    end_signal.set()


def frame_handler(cam, frame, pic_name):
    # 如果更改了图片则保存此帧，否则不做任何事
    if change.is_set():
        frame.convert_pixel_format(px_format)
        # 保存图片
        cv2.imwrite(os.path.join(fruit_dir, pic_name), frame.as_opencv_image())
        change.clear()
    cam.queue_frame(frame)


if __name__ == '__main__':
    change = threading.Event()
    end_signal = threading.Event()

    t1 = threading.Thread(target=picshowting_thread, args=(change, ))
    t2 = threading.Thread(target=camera.shootting_thread, args=(end_signal, frame_handler, exposure_time, gain, end_signal,))

    t1.start()
    t2.start()

