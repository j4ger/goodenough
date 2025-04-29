import numpy as np
from ultralytics import YOLOE
from ultralytics.models.yolo.yoloe import YOLOEVPSegPredictor
import supervision as sv
import cv2

# Initialize a YOLOE model
model = YOLOE("yoloe-11m-seg.pt")

# Define visual prompts based on a separate reference image
visual_prompts = dict(
    bboxes=np.array([[0, 0, 158, 158]]),
    cls=np.array([0]),
)

target = cv2.imread("assets/raw/1.png")

# Run prediction on a different image, using reference image to guide what to look for
results = model.predict(
    target,  # Target image for detection
    refer_image="assets/profiles/小寄居蟹.png",  # Reference image used to get visual prompts
    visual_prompts=visual_prompts,
    predictor=YOLOEVPSegPredictor,
)

print(results)

detections = sv.Detections.from_ultralytics(results[0])

mask_annotator = sv.MaskAnnotator()
label_annotator = sv.LabelAnnotator(text_position=sv.Position.CENTER)

annotated_image = mask_annotator.annotate(
    scene=target, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections)

cv2.imwrite("output.png", annotated_image)
