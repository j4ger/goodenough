from ultralytics import YOLO
from aux import imgshow
from db import db
import pytesseract
from ocr import crop_and_ocr

model = YOLO("./model.pt")

L1_NUMBER = (467, 1370, 467 + 67, 1370 + 26)
L2_NUMBER = (570, 1370, 570 + 67, 1370 + 26)
L3_NUMBER = (673, 1370, 673 + 67, 1370 + 26)
R1_NUMBER = (938, 1370, 938 + 67, 1370 + 26)
R2_NUMBER = (1050, 1370, 1050 + 67, 1370 + 26)
R3_NUMBER = (1153, 1370, 1153 + 67, 1370 + 26)

PARTICIPANTS = (400, 1271, 400 + 886, 1271 + 150)
MAP = (0, 0, 1680, 1250)


def parse_participants(image):
    cropped = image.crop(PARTICIPANTS)
    detections = model(cropped)[0]

    counts = []
    for region in [L1_NUMBER, L2_NUMBER, L3_NUMBER, R1_NUMBER, R2_NUMBER, R3_NUMBER]:
        text = (
            crop_and_ocr(
                image, region, invert=True, threshold=170, allowlist="x0123456789"
            )
            .replace("x", "")
            .replace(" ", "")
        )
        counts.append(int(text))
    out = []
    for index, result in enumerate(detections.summary()):
        # find the entry with same name in db
        for entry in db:
            if entry["name"] == result["name"]:
                participant = {
                    "count": counts[index],
                    "id": entry["id"],
                    "name": entry["name"],
                }
                out.append(participant)
                break
    return out


def parse_locations(image):
    cropped = image.crop(MAP)
    detections = model(cropped)[0]

    results = {}


# TODO: bounding boxes
