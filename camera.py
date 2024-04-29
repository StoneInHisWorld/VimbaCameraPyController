import time
from VimbaPython.Source.vimba import *


class VimbaCamera:

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

    def shoot(self, px_format=PixelFormat.Mono8, timeout=2000):
        """
        同步单帧拍照，每次拍照之前对相机参数进行更新。
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
                    yield frame

    def AS_shoot(self, start_signal, end_signal, frame_handler):
        """异步拍摄，适用于多线程程序。
        请将此方法作为线程的target参数值。
        :param start_signal: 开始信号。用于给相机预留出足够的初始化时间，会在相机开始帧接收后检查start_signal的值。
        :param end_signal: 结束信号，通知相机结束拍摄。
        :param frame_handler: 单帧处理方法，使用该方法处理相机获取的每一帧。接口必须为def handler(cam, frame)->None
        :return: None
        """
        with Vimba.get_instance() as vimba:
            cams = vimba.get_all_cameras()
            with cams[0] as cam:
                self.__update_param(cam)
                # TODO：frame_handler需要屏蔽vimba接口相关
                cam.start_streaming(frame_handler)
                start_signal.wait()
                end_signal.wait()
                time.sleep(1)
                cam.stop_streaming()

    def __update_param(self, cam):
        cam_expostime = cam.ExposureTimeAbs
        cam_gain = cam.Gain
        cam_expostime.set(self.__exposTime)
        cam_gain.set(self.__gain)
