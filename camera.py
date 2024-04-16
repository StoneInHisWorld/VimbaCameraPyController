from VimbaPython.Source.vimba import *


class Camera:

    def __init__(self, no):
        """
        初始化Vimba相机
        :param no: 取当前连接的第no号相机
        """
        self.__no = no
        self.__exposTime = 50
        self.__gain = 0
        self.__close = False
        with Vimba.get_instance() as vimba:
            cams = vimba.get_all_cameras()
            assert len(cams) >= 1, 'No camera detected!'
            self.__device = cams[no]

    def set_exposTime(self, exposTime):
        """
        设置相机曝光时间
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

    def shoot(self, px_format=PixelFormat.Mono8, timeout=2000) -> Frame:
        """
        同步单帧拍照
        :param px_format: 帧像素格式，一般设置为PixelFormat.Mono8
        :param timeout: 拍照超时时间，超过时间则判定为相机出错。
        :return: 拍照帧
        """
        self.__close = False
        with self.__device as cam:
            while not self.__close:
                self.__update_param(cam)
                frame = cam.get_frame(timeout)
                frame.convert_pixel_format(px_format)
                yield frame

    def __update_param(self, cam):
        cam_expostime = cam.ExposureTimeAbs
        cam_gain = cam.Gain
        cam_expostime.set(self.__exposTime)
        cam_gain.set(self.__gain)

    def close(self):
        self.__close = True


# Synchronous grab
def shoot(exposure_time=50, gain=0, px_format=PixelFormat.Mono8):
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        assert len(cams) >= 1, 'No camera detected!'
        with cams[0] as cam:
            cam_expostime = cam.ExposureTimeAbs
            cam_gain = cam.Gain
            cam_expostime.set(exposure_time)
            cam_gain.set(gain)

            # Aquire single frame synchronously
            frame = cam.get_frame()
            frame.convert_pixel_format(px_format)
            # print(frame.as_numpy_ndarray())
            return frame


# Asynchronous grab
def shootting_thread(end_signal, frame_handler, exposure_time=50, gain=0):
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        with cams[0] as cam:
            # set camera
            cam_exposuretime = cam.ExposureTimeAbs
            cam_gain = cam.Gain
            cam_exposuretime.set(exposure_time)
            cam_gain.set(gain)

            cam.start_streaming(frame_handler)
            end_signal.wait()
            cam.stop_streaming()
