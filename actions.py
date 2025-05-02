import cv2 as cv
from device import device, click
import time
from ocr import (
    test_pregame,
    test_ingame,
    test_end,
    test_home,
    test_mode_select,
    test_left_win,
    test_right_win,
)
from enum import Enum
from PIL import Image

BUTTON_VOTE_LEFT = (219, 1333)
BUTTON_VOTE_RIGHT = (1469, 1333)
BUTTON_OBSERVE = (840, 850)
BUTTON_RETURN = (1469, 1333)
BUTTON_JOIN = (1405, 1279)
BUTTON_MODE_SELECT = (1118, 1150)
BUTTON_START = (1562, 1156)

INTERVAL = 0.8


class State(Enum):
    PREGAME = 0
    INGAME = 1
    LEFT_WIN = 2
    RIGHT_WIN = 3
    END = 4
    HOME = 5
    MODE_SELECT = 6
    UNKNOWN = 7


def keep_in_match(frame):
    if test_pregame(frame):
        print("[state] pre game")
        click(BUTTON_OBSERVE)
        print("[action] voting observe")
        return State.PREGAME
    if test_ingame(frame):
        print("[state] in game")
        return State.INGAME
    if test_left_win(frame):
        print("[state] left win")
        return State.LEFT_WIN
    if test_right_win(frame):
        print("[state] right win")
        return State.RIGHT_WIN
    if test_end(frame):
        print("[state] end game")
        click(BUTTON_RETURN)
        print("[action] returning")
        return State.END
    if test_home(frame):
        print("[state] home")
        click(BUTTON_JOIN)
        print("[action] joining")
        return State.HOME
    if test_mode_select(frame):
        print("[state] mode select")
        click(BUTTON_MODE_SELECT)
        print("[action] selecting mode")
        time.sleep(0.1)
        click(BUTTON_START)
        print("[action] starting game")
        return State.MODE_SELECT
    print("[state] unknown")
    return State.UNKNOWN


def event_loop():
    with open("assets/replays/nextval", "r") as f:
        nextval = int(f.read())

    frame = Image.fromarray(cv.cvtColor(device.last_frame, cv.COLOR_BGR2RGB))
    state = keep_in_match(frame)
    exit = False
    game_frame = frame
    while not exit:
        frame = Image.fromarray(cv.cvtColor(device.last_frame, cv.COLOR_BGR2RGB))
        new_state = keep_in_match(frame)
        if state != State.PREGAME and new_state == State.PREGAME:
            game_frame = frame
        if state == State.INGAME:
            if new_state == State.LEFT_WIN:
                save_data(game_frame, True, nextval)
                nextval += 1
            if new_state == State.RIGHT_WIN:
                save_data(game_frame, False, nextval)
                nextval += 1
        if new_state != State.UNKNOWN and new_state != State.PREGAME:
            state = new_state
        time.sleep(INTERVAL)


def save_data(image, left_win, nextval):
    print(f"[dataset] new data: {nextval}")
    image.save(f"assets/replays/images/{nextval}.png", "PNG")
    with open(f"assets/replays/results/{nextval}", "w") as f:
        f.write(str(left_win))

    with open("assets/replays/nextval", "w") as f:
        f.write(str(nextval))
