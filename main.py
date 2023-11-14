import datetime
import time

import cv2

from VimbaPython.Source.vimba import *

cam_exposuretime = 50
cam_gain = 0


def frame_handler(cam, frame):
    frame.convert_pixel_format(PixelFormat.Mono8)
    print(frame.as_numpy_ndarray())
    to_be_save = frame.as_opencv_image()
    cv2.imwrite(f'./fruits/{frame.get_id()}.jpg', to_be_save)
    cam.queue_frame(frame)


with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()
    with cams[0] as cam:
        # set camera
        exposure_time = cam.ExposureTimeAbs
        gain = cam.Gain
        exposure_time.set(cam_exposuretime)
        gain.set(cam_gain)

        cam.start_streaming(frame_handler)
        time.sleep(5)
        cam.stop_streaming()
