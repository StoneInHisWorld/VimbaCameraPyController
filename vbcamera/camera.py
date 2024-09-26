import time

from VimbaPython.Source.vimba import *


class VimbaCamera:
    """Vimba相机对象，封装了支持vimba接口的相机提供的基础功能"""

    def __init__(self, no, expos_time=50, gain=0):
        """Vimba相机对象，初始化时会检查相机是否已经进行连接。

        :param no: 取当前连接的第no号相机
        :param expos_time: 相机的曝光时间
        :param gain: 相机的增益值
        """
        self.__no = no
        self.__exposTime = expos_time
        self.__gain = gain
        self.__close = False
        with Vimba.get_instance() as vimba:
            try:
                _ = vimba.get_all_cameras()[no]
                print(f'已连接上{no}号相机！')
            except IndexError:
                raise ConnectionError(f'{no}号相机未连接！')

    def set_exposTime(self, exposTime):
        """设置相机曝光时间

        :param exposTime: 曝光时间
        :return: None
        """
        self.__exposTime = exposTime

    def set_gain(self, gain):
        """设置相机增益。

        :param gain: 增益
        :return: None
        """
        self.__gain = gain

    def syn_shoot(self, px_format=PixelFormat.Mono8, timeout=2000):
        """同步单帧拍照，
        通过迭代器的next()调用来进行拍照，每次拍照之前会对相机参数进行更新
        拍照后会把单帧转换成`numpy.ndarray`返回

        :param px_format: 帧像素格式，一般设置为PixelFormat.Mono8
        :param timeout: 拍照超时时间，超过时间则判定为相机出错。
        :return: 不断提供拍照帧的生成器
        """
        # TODO：Untested!
        with Vimba.get_instance() as vimba:
            cams = vimba.get_all_cameras()
            with cams[0] as cam:
                while True:
                    self.__update_param(cam)
                    frame = cam.get_frame(timeout)
                    frame.convert_pixel_format(px_format)
                    yield frame.as_opencv_image()

    def asyn_shoot(self, start_signal, end_signal, frame_handler):
        """异步拍摄，适用于多线程程序。
        通过设置`start_signal`启动相机拍摄，每帧经过`frame_handler`处理前会更新相机参数。
        在线程外设置`end_signal`以结束相机拍摄。

        :param start_signal: 所有设备开始信号。
            用于给相机预留出足够的初始化时间，会在相机开始帧接收后检查start_signal的值。
        :param end_signal: 所有设备结束信号，通知相机结束拍摄。
        :param frame_handler: 单帧处理方法，使用该方法处理相机获取的每一帧。签名需为：
            def handler(cam, frame)
        :return: None
        """
        # TODO: UNTESTED!
        with Vimba.get_instance() as vimba:
            cams = vimba.get_all_cameras()
            with cams[0] as cam:
                # self.__update_param(cam)
                def handler_impl(cam, frame):
                    self.__update_param(cam)
                    frame_handler(cam, frame)

                cam.start_streaming(handler_impl)
                start_signal.wait()
                end_signal.wait()
                time.sleep(1)
                cam.stop_streaming()

    def __update_param(self, cam):
        """更新相机的参数"""
        cam_expostime = cam.ExposureTimeAbs
        cam_gain = cam.Gain
        cam_expostime.set(self.__exposTime)
        cam_gain.set(self.__gain)
