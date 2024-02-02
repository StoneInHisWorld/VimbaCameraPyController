import os
import time

from tqdm import tqdm

import picshow
from VimbaPython.Source.vimba import PixelFormat
from camera import Camera

"""设置相机参数"""
gain = 23
exposTime = 300000
px_format = PixelFormat.Mono8
timeout = 300000

"""设置图片展示参数"""
dataset_path = './data'
fruit_root = './fruits'
path_iter = os.walk(dataset_path)
_, _, files = next(path_iter)

# 获取屏幕尺寸并设置好plt属性
screen_size = picshow.get_screen_size()
print(screen_size)
picshow.prepare_plt(screen_size=screen_size, win_size=(770, 960))

for wait in range(3, 0, -1):
    print(f'\r实验将在{wait}秒后开始，请做好准备！', flush=True, end='')
    time.sleep(1)

# TODO:初始化相机
camera = Camera(0)
camera.set_exposTime(exposTime)
camera.set_gain(gain)

# 流水线
with tqdm(files, desc='打开图片...', unit='张', position=0, leave=True) as pbar:
    frame_iter = camera.shoot(px_format, timeout)
    for fn in pbar:
        # TODO:显示图片
        pbar.set_description(f'处理{fn}')

        # 拍照，获取帧
        frame = next(frame_iter)

        # TODO: 帧处理
