from typing import List
import numpy as np
import supervision as sv
from PIL import Image

def plot(image: np.ndarray, detections, classes: List[str], raw=False):
    """
    Plot bounding boxes or segmentation masks on an image.

    Args:
        image: The image to plot on
        detections: The detections to plot
        classes: The classes to plot
        raw: Whether to return the raw image or plot it interactively

    Returns:
        The raw image (np.ndarray) if raw=True, otherwise None (image is plotted interactively
    """
    # TODO: When we have a classification annotator
    # in supervision, we can add it here
    if detections.mask is not None:
        annotator = sv.MaskAnnotator()
    else:
        annotator = sv.BoxAnnotator()

    label_annotator = sv.LabelAnnotator()

    labels = [
        f"{classes[class_id]} {confidence:0.2f}"
        for _, _, confidence, class_id, _, _ in detections
    ]

    annotated_frame = annotator.annotate(scene=image.copy(), detections=detections)
    annotated_frame = label_annotator.annotate(
        scene=annotated_frame, labels=labels, detections=detections
    )

    if raw:
        return annotated_frame

    result = Image.fromarray(annotated_frame)
    result.save("output.png")
