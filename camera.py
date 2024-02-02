import threading
from typing import Callable

from VimbaPython.Source.vimba import *


class Camera:

    def __init__(self, no):
        """
        Vimba相机封装类，提供方便但有限的接口以供vimba接口相机的使用。

        提供shoot()以及AS_shoot()方法进行帧获取，在使用前请使用setter函数进行相机参数设置。
        :param no: 取当前连接的第 no号相机
        """
        self.__no = no
        self.__exposTime = 50
        self.__gain = 0
        self.__close = False

    def set_exposTime(self, exposTime):
        """
        设置相机曝光时间。
        :param exposTime: 曝光时间
        :return: None
        """
        self.__exposTime = exposTime

    def set_gain(self, gain):
        """
        设置相机增益。
        :param gain: 增益
        :return: None
        """
        self.__gain = gain

    def shoot(self, px_format=PixelFormat.Mono8, timeout=2000):
        """
        同步单帧拍照，使用 `for frame in camera.shoot():`获取每一帧。

        for循环的每次执行都会更新相机参数。请通过setter方法设置相机参数，新的相机参数将会在下一帧实施。
        :param px_format: 帧像素格式，一般设置为`PixelFormat.Mono8`
        :param timeout: 拍照超时时间，超过时间则判定为相机出错。
        :return: 拍照帧迭代器。
        """
        with Vimba.get_instance() as vimba:
            # 初始化相机
            cams = vimba.get_all_cameras()
            assert len(cams) >= 1, '没有检测到相机，请检查相机接口！'
            with cams[self.__no] as cam:
                # 更新相机参数以及拍照超时时间
                self.__update_param(cam)
                timeout = 2 * self.__exposTime if self.__exposTime >= timeout else timeout
                frame = cam.get_frame(timeout)
                frame.convert_pixel_format(px_format)
                yield frame

    def AS_shoot(self, handler: Callable, end: threading.Event):
        """
        相比同步拍照，本异步拍照方法更为高效。vimba接口从相机获取帧，通过 handler方法进行处理。本程序通过end信号控制程序的结束。

        本函数一旦调用，则不可修改相机参数！
        :param handler: 帧处理器，将vimba接口传入的相机对象和帧对象进行处理。签名需为：def handler(cam, frame) -> None
        :param end: 结束信号，用以结束帧获取程序。
        :return: None
        """
        with Vimba.get_instance() as vimba:
            # 初始化相机
            cams = vimba.get_all_cameras()
            assert len(cams) >= 1, '没有检测到相机，请检查相机接口！'
            with cams[self.__no] as cam:
                # 设置相机参数
                cam_expostime = cam.ExposureTimeAbs
                cam_gain = cam.Gain
                cam_expostime.set(self.__exposTime)
                cam_gain.set(self.__gain)
                # 相机开始拍照
                cam.start_streaming(handler)
                end.wait()
                cam.stop_streaming()

    def __update_param(self, cam):
        """
        更新相机参数。外部请通过setter进行相机参数更新。
        :param cam: 需要更改参数的相机。
        :return: None
        """
        cam_expostime = cam.ExposureTimeAbs
        cam_gain = cam.Gain
        cam_expostime.set(self.__exposTime)
        cam_gain.set(self.__gain)


# # Synchronous grab
# def shoot(exposure_time=50, gain=0, px_format=PixelFormat.Mono8):
#     with Vimba.get_instance() as vimba:
#         cams = vimba.get_all_cameras()
#         assert len(cams) >= 1, 'No camera detected!'
#         with cams[0] as cam:
#             cam_expostime = cam.ExposureTimeAbs
#             cam_gain = cam.Gain
#             cam_expostime.set(exposure_time)
#             cam_gain.set(gain)
#
#             # Aquire single frame synchronously
#             frame = cam.get_frame()
#             frame.convert_pixel_format(px_format)
#             # print(frame.as_numpy_ndarray())
#             return frame
#
#
# # Asynchronous grab
# def shootting_thread(end_signal, frame_handler, exposure_time=50, gain=0):
#     with Vimba.get_instance() as vimba:
#         cams = vimba.get_all_cameras()
#         with cams[0] as cam:
#             # set camera
#             cam_exposuretime = cam.ExposureTimeAbs
#             cam_gain = cam.Gain
#             cam_exposuretime.set(exposure_time)
#             cam_gain.set(gain)
#
#             cam.start_streaming(frame_handler)
#             end_signal.wait()
#             cam.stop_streaming()
