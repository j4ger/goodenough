import scrcpy
from adbutils import adb
import time

device = scrcpy.Client(device=adb.device_list()[0], max_fps=20)


def click(pos):
    device.control.touch(pos[0], pos[1], scrcpy.ACTION_DOWN)
    time.sleep(0.02)
    device.control.touch(pos[0], pos[1], scrcpy.ACTION_UP)
