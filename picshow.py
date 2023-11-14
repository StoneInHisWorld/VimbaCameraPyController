import os
import time

import cv2
import pyautogui
import PIL.Image
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm

matplotlib.use('TkAgg')


def get_screen_size():
    screen_width, screen_height = pyautogui.size()
    return screen_height, screen_width
    # mgr = plt.get_current_fig_manager()
    # mgr.full_screen_toggle()
    # height = mgr.canvas.height()
    # width = mgr.canvas.width()
    # return height, width


def find_open_pic(path):
    img = PIL.Image.open(path)
    plt.imshow(img, cmap='gray', aspect='equal')


def prepare_plt(pos=(0, 0), screen_size=None, win_size=None):
    # plt.rcParams['figure.figsize'] = (0.28, 0.28)
    # plt.figure(dpi=150)
    # 设置窗口位置
    manager = plt.get_current_fig_manager()
    if screen_size is not None:
        pos = (screen_size[1]//2 - win_size[1]//2, screen_size[0]//2 - win_size[0]//2)
    manager.window.wm_geometry(f"+{pos[0]}+{pos[1]}")


def show_pic(path, sleep=1):
    # 设置互动模式以及窗口内属性
    plt.ion()
    plt.axis('off')
    # 打开图片
    find_open_pic(path)
    time.sleep(sleep)
    plt.pause(sleep)
    plt.clf()
    # 退出动作
    plt.ioff()


# def close_pic():
#     plt.clf()
#     # plt.close()
#     # 退出动作
#     plt.ioff()


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
            # show_pic(path, sleep=0.5, screen_size=screen_size, win_size=(200, 200))
            show_pic(path, sleep=0.5)
            cv2.destroyAllWindows()


def get_pic_names(dataset_dir):
    path_iter = os.walk(dataset_dir)
    _, __, file_names = next(path_iter)
    return sorted(
        file_names, key=lambda name: int(name.split(".")[0])
    )  # 给文件名排序！