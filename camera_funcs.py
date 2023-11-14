from time import sleep

import numpy as np
import cv2

from VimbaPython.Source.vimba import *


# @ScopedLogEnable(LOG_CONFIG_INFO_CONSOLE_ONLY)
# def print_device_id(dev, state):
#     msg = 'Device: {}, State: {}'.format(str(dev), str(state))
#     Log.get_instance().info(msg)
#
#
# vimba = Vimba.get_instance()
# vimba.register_camera_change_handler(print_device_id)
# vimba.register_interface_change_handler(print_device_id)
#
# with vimba:
#     sleep(10)


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
