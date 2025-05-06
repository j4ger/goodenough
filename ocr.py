from PIL import Image, ImageOps
from aux import imgshow
import cv2 as cv
import numpy as np
import pytesseract

HEIGHT = 1680
WIDTH = 1440

PREGAME_LABEL = (785, 1254, 785 + 109, 1254 + 48)
PREGAME_LABEL_CONTENT = "ROUND"

INGAME_LABEL = (149, 1386, 149 + 141, 1386 + 44)
INGAME_LABEL_CONTENT = "支持此队伍"

END_LABEL = (1395, 1362, 1395 + 148, 1362 + 50)
END_LABEL_CONTENT = "返回主页"

HOME_LABEL = (1471, 1318, 1471 + 134, 1318 + 48)
HOME_LABEL_CONTENT = "加入赛事"

MODE_LABEL = (440, 404, 440 + 202, 404 + 58)
MODE_LABEL_CONTENT = "选择赛事"

RESULT_LABEL = (4, 738, 4 + 382, 738 + 142)
RESULT_LABEL_CONTENT = "WINLOSE"


def crop_and_ocr(
    image, region, invert=False, threshold=150, chn=False, allowlist=None, psm=6, oem=0
):
    cropped = image.crop(region)
    cropped = np.array(cropped)
    greyscaled = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
    method = cv.THRESH_BINARY_INV if invert else cv.THRESH_BINARY
    thresholded = cv.threshold(greyscaled, threshold, 255, method)[1]
    lang = "eng+chi_sim" if chn else "eng"
    config = (
        f"-c tessedit_char_whitelist={allowlist} --psm {psm} --oem {oem}"
        if allowlist is not None
        else f"--psm {psm} --oem {oem}"
    )

    results = (
        pytesseract.image_to_string(thresholded, lang=lang, config=config)
        .strip()
        .replace(" ", "")
    )

    return results


def test_ingame(image):
    text = crop_and_ocr(
        image,
        INGAME_LABEL,
        threshold=80,
        invert=True,
        oem=1,
        chn=True,
        allowlist=INGAME_LABEL_CONTENT,
    )

    return text == INGAME_LABEL_CONTENT and not test_pregame(image)


def test_pregame(image):
    text = crop_and_ocr(
        image,
        PREGAME_LABEL,
        threshold=200,
        oem=1,
        invert=True,
        allowlist=PREGAME_LABEL_CONTENT,
    )
    return text == PREGAME_LABEL_CONTENT


def test_end(image):
    text = crop_and_ocr(
        image, END_LABEL, threshold=120, oem=1, chn=True, allowlist=END_LABEL_CONTENT
    )
    return text == END_LABEL_CONTENT


def test_home(image):
    text = crop_and_ocr(
        image, HOME_LABEL, threshold=60, oem=1, chn=True, allowlist=HOME_LABEL_CONTENT
    )
    return text == HOME_LABEL_CONTENT


def test_mode_select(image):
    text = crop_and_ocr(
        image,
        MODE_LABEL,
        threshold=130,
        oem=1,
        chn=True,
        invert=True,
        allowlist=MODE_LABEL_CONTENT,
    )
    return text == MODE_LABEL_CONTENT


def test_left_win(image):
    text = crop_and_ocr(
        image,
        RESULT_LABEL,
        threshold=170,
        oem=1,
        invert=True,
        allowlist=RESULT_LABEL_CONTENT,
    )
    return text == "WIN"


def test_right_win(image):
    text = crop_and_ocr(
        image,
        RESULT_LABEL,
        threshold=110,
        oem=1,
        invert=True,
        allowlist=RESULT_LABEL_CONTENT,
    )
    return text == "LOSE"
