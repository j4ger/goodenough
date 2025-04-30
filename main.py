import scrcpy
from adbutils import adb
from rich.console import Console
from textual_image.renderable import Image as SImage
import cv2
import time
from PIL import Image
import easyocr

HEIGHT = 1680
WIDTH = 1440

BUTTON_VOTE_LEFT = (219, 1333)
BUTTON_VOTE_RIGHT = (1469, 1333)
BUTTON_RETURN = (1469, 1333)
BUTTON_JOIN = (1405, 1279)
BUTTON_MODE_SELECT = (285, 1150)
BUTTON_START = (1562, 1156)

INGAME_LABEL = ((785, 1254), (785 + 109, 1254 + 48))
INGAME_LABEL_CONTENT = "round"

END_LABEL = ((67, 143), (67 + 98, 143 + 36))
END_LABEL_CONTENT = "比赛结束"

HOME_LABEL = ((1471, 1318), (1471 + 134), (1318 + 48))
HOME_LABEL_CONTENT = "加入赛事"

MODE_LABEL = ((360, 1181), (360 + 127, 1181 + 41))
MODE_LABEL_CONTENT = "竞猜对决"

RESULT_LABEL = ((4, 738), (4 + 382, 738 + 142))
RESULT_LEFT_WIN_LABEL = "win"
RESULT_RIGHT_WIN_LABEL = "lose"

device = scrcpy.Client(device=adb.device_list()[0])
console = Console()
ocr = easyocr.Reader(["ch_sim", "en"])


def main():
    device.start(threaded=True)
    print("resolution: ", device.resolution)
    while True:
        if device.last_frame is not None:
            console.print(
                SImage(
                    Image.fromarray(cv2.cvtColor(device.last_frame, cv2.COLOR_BGR2RGB))
                )
            )
        time.sleep(0.5)


if __name__ == "__main__":
    main()
