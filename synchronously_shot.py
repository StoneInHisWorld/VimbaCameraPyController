import os
import time

import cv2
from tqdm import tqdm

import picshow
import camera as camera

# 打开数据库中的图片并进行显示
from picshow import get_pic_names

dataset_dir = './data/MNIST'
fruit_dir = './fruits/{}'.format(time.strftime('%Y-%m-%d-%H.%M', time.localtime()))
# figsize = (0.3, 0.3)
exposure_time = 70
gain = 1

print('请准备好进行数据采集...')
time.sleep(10)

# 获取屏幕尺寸并设置好plt属性
screen_size = picshow.get_screen_size()
print(screen_size)
picshow.prepare_plt(screen_size=screen_size, win_size=(770, 960))

# 流水线
file_names = get_pic_names(dataset_dir)
with tqdm(file_names, desc='打开图片...', unit='img', position=0, leave=True) as pbar:
    for fn in pbar:
        # 显示
        pbar.set_description(f'处理{fn}')
        # pbar.set_description(f'打开{fn}')
        path = os.path.join(dataset_dir, fn)
        picshow.show_pic(path, sleep=0.1)

        # 拍照
        # pbar.set_description(f'拍下{fn}')
        frame = camera.shoot(exposure_time=exposure_time, gain=gain)

        # 存图
        if not os.path.exists(fruit_dir):
            os.mkdir(fruit_dir)
        # pbar.set_description(f'保存{fn}')
        cv2.imwrite(os.path.join(fruit_dir, fn), frame.as_opencv_image())
