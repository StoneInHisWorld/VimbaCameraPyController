import cv2
import matplotlib
import matplotlib.pyplot as plt
import pyautogui

matplotlib.use('TkAgg')


def get_screen_size():
    """
    获取屏幕尺寸
    :return: （屏幕高度，屏幕宽度）
    """
    screen_width, screen_height = pyautogui.size()
    return screen_height, screen_width


def find_open_pic(path):
    """
    根据路径打开图片并显示
    :param path: 图片路径
    :return: None
    """
    return cv2.imread(path)


def prepare_plt(pos=(0, 0), screen_size=None, win_size=None):
    """
    初始化matplotlib
    :param pos: 窗口展示位置（左上角）
    :param screen_size: 屏幕大小
    :param win_size: 窗口大小
    :return: None
    """
    # 设置窗口位置
    manager = plt.get_current_fig_manager()
    if screen_size is not None:
        pos = (screen_size[1]//2 - win_size[1]//2, screen_size[0]//2 - win_size[0]//2)
    manager.window.wm_geometry(f"+{pos[0]}+{pos[1]}")


def show_pic(pic, sleep=0.1):
    """
    展示图片
    :param pic: 待展示图片
    :param sleep: 图片动画停止时间，设置为0则图片不会停留在窗口。
    :return: None
    """
    # 设置互动模式以及窗口内属性
    plt.ion()
    plt.axis('off')
    # 打开图片
    if pic is str:
        pic = find_open_pic(pic)
    plt.imshow(pic, cmap='gray', aspect='equal')
    plt.pause(sleep)
    plt.clf()
    # 退出动作
    plt.ioff()


# if __name__ == '__main__':
#     img_dir = './data/MNIST'
#     path_iter = os.walk(img_dir)
#     _, __, file_names = next(path_iter)
#     file_names = sorted(
#         file_names, key=lambda name: int(name.split(".")[0])
#     )  # 给文件名排序！
#     # 获取屏幕尺寸
#     screen_size = get_screen_size()
#     print(screen_size)
#     figsize=(30, 30)
#     with tqdm(file_names, desc='打开图片...', unit='img', position=0, leave=True) as pbar:
#         prepare_plt(screen_size=screen_size, win_size=(770, 960))
#         for fn in pbar:
#             pbar.set_description(f'打开{fn}')
#             path = os.path.join(img_dir, fn)
#             # show_pic(path, sleep=0.5, screen_size=screen_size, win_size=(200, 200))
#             show_pic(path, sleep=0.5)
#             cv2.destroyAllWindows()
#
#
# def get_pic_names(dataset_dir):
#     path_iter = os.walk(dataset_dir)
#     _, __, file_names = next(path_iter)
#     return sorted(
#         file_names, key=lambda name: int(name.split(".")[0])
#     )  # 给文件名排序！