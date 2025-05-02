from actions import event_loop
from device import device
import time


def main():
    device.start(threaded=True)
    print("resolution: ", device.resolution)
    # while True:
    #     if device.last_frame is not None:
    #         console.print(
    #             SImage(
    #                 Image.fromarray(cv2.cvtColor(device.last_frame, cv2.COLOR_BGR2RGB))
    #             )
    #         )
    #     time.sleep(0.5)
    # for i in range(1, 40):
    #     result = parse_participants(Image.open(f"./assets/raw/{i}.png"))
    #     print(f"result {i}: {result}")
    while True:
        if device.last_frame is None:
            print("[init] no frame yet")
            time.sleep(0.5)
        else:
            break
    print("[init] starting event loop")
    event_loop()


if __name__ == "__main__":
    main()
