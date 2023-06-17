import logging
from collections import deque
from math import sqrt
from datetime import datetime
import os

from pyautogui import screenshot
from PIL import ImageChops
from PIL.Image import Image
import numpy as np

from utils import log_times

logger = logging.getLogger(__name__)
queue = deque(maxlen=2)


@log_times
def _screen_analysis(diff_threshold_percentage: int, image_folder: str):
    img = screenshot()
    img = img.convert("RGB")
    queue.append(img)
    if len(queue) > 1:
        diff = compare_images(queue[0], queue[1])
        logger.info(f"{diff = :.2%}")
        print(f"diff: {diff:.2%}")
        if diff > diff_threshold_percentage / 100:
            os.makedirs(image_folder, exist_ok=True)
            file_path = f"{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.jpeg"
            logging.info(f"{file_path = }")
            print(f"Saved image: {file_path}")
            img.save(os.path.join(image_folder, file_path), quality=70)


@log_times
def compare_images(img1: Image, img2: Image) -> float:
    diff_image = ImageChops.difference(img1, img2)
    diff = np.asarray(diff_image, dtype=np.half) / 255  # type: ignore
    mse = sqrt(np.mean(np.square(diff)))
    return mse
