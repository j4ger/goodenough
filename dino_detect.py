from autodistill_clip import CLIP
from autodistill.detection import CaptionOntology
from autodistill_grounding_dino import GroundingDINO
from autodistill.core import EmbeddingOntologyImage
from plot import plot
from distill_base import ComposedDetectionModel

import torch
import clip
from PIL import Image
import os
import cv2

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

with open("enemies.txt", "r") as f:
    enemies = f.read().splitlines()

image_mapping = {}
for index, name in enumerate(enemies):
    image_mapping[index] = f"{name}.png"

embeddings_to_classes = {}


model = ComposedDetectionModel(
    detection_model=GroundingDINO(
        CaptionOntology({"mob": "output", "animal": "output", "human": "output", "vehicle": "output", "character": "output"})
    ),
    classification_model=CLIP(
        EmbeddingOntologyImage(embeddings_to_classes)
    )
)

test_image="./assets/raw/2.png"

result = model.predict(test_image)

print("Detected objects: ", result)

plot(
    image=cv2.imread(test_image),
    detections=result,
    classes=list(image_mapping.keys())
)
