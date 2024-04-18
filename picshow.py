import os
import time

import PIL
import cv2
import pyautogui
import PIL.Image as IMAGE
from PIL.Image import Image
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm

matplotlib.use('TkAgg')


def get_screen_size():
    screen_width, screen_height = pyautogui.size()
    return screen_height, screen_width


def find_open_pic(path_or_img, img_transformer):
    if isinstance(path_or_img, str):
        img = PIL.Image.open(path_or_img)
    elif isinstance(path_or_img, Image):
        img = path_or_img
    else:
        raise NotImplementedError(f"不明值{path_or_img}")
    img = img_transformer(img)
    plt.imshow(img, cmap='gray', aspect='equal')


def binarize_img(img: Image, threshold: int = 127) -> Image:
    """
    将图片根据阈值进行二值化
    参考自：https://www.jianshu.com/p/f6d40a73310f
    :param img: 待转换图片
    :param threshold: 二值图阈值
    :return: 转换好的图片
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    # 图片二值化
    return img.point(table, '1')


def prepare_plt(pos=(0, 0), screen_size=None, win_size=None, **fig_kwargs):
    # 设置窗口位置
    manager = plt.get_current_fig_manager()
    if screen_size is not None:
        pos = (screen_size[1]//2 - win_size[1]//2, screen_size[0]//2 - win_size[0]//2)
    manager.window.wm_geometry(f"+{pos[0]}+{pos[1]}")
    plt.figure(**fig_kwargs)


def show_pic(path, sleep=1, img_transformer=lambda i: i):
    # 设置互动模式以及窗口内属性
    plt.ion()
    plt.axis('off')
    # 打开图片
    find_open_pic(path, img_transformer)
    time.sleep(sleep)
    plt.pause(sleep)
    plt.clf()
    # 退出动作
    plt.ioff()


if __name__ == '__main__':
    img_dir = './data/MNIST'
    path_iter = os.walk(img_dir)
    _, __, file_names = next(path_iter)
    file_names = sorted(
        file_names, key=lambda name: int(name.split(".")[0])
    )  # 给文件名排序！
    # 获取屏幕尺寸
    screen_size = get_screen_size()
    print(screen_size)
    figsize=(30, 30)
    with tqdm(file_names, desc='打开图片...', unit='img', position=0, leave=True) as pbar:
        prepare_plt(screen_size=screen_size, win_size=(770, 960))
        for fn in pbar:
            pbar.set_description(f'打开{fn}')
            path = os.path.join(img_dir, fn)
            show_pic(path, sleep=0.5)
            cv2.destroyAllWindows()


def get_pic_names(dataset_dir):
    path_iter = os.walk(dataset_dir)
    _, __, file_names = next(path_iter)
    return sorted(
        file_names, key=lambda name: int(name.split(".")[0])
    )  # 给文件名排序！