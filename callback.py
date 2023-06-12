import logging
from collections import deque
from math import sqrt
from datetime import datetime
from time import sleep
import os

from pyautogui import screenshot
from PIL import ImageChops
from PIL.Image import Image
import numpy as np

from utils import log_times

IMAGE_FOLDER = "images"
DIFF_THRESHOLD = 0.3
TIME_INTERVAL_SEC = 5

queue = deque(maxlen=2)


def periodic_screen_analysis():
    while True:
        screen_analysis()
        sleep(TIME_INTERVAL_SEC)


@log_times
def screen_analysis():
    img = screenshot()
    img = img.convert("RGB")
    queue.append(img)
    if len(queue) > 1:
        diff = compare_images(queue[0], queue[1])
        logging.info(f"{diff = :.2%}")
        if diff > DIFF_THRESHOLD:
            os.makedirs(IMAGE_FOLDER, exist_ok=True)
            file_path = f"{datetime.now().isoformat()}.jpeg"
            logging.info(f"{file_path = }")
            img.save(os.path.join(IMAGE_FOLDER, file_path), quality=70)


@log_times
def compare_images(img1: Image, img2: Image) -> float:
    diff_image = ImageChops.difference(img1, img2)
    diff = np.asarray(diff_image, dtype=np.half) / 255  # type: ignore
    mse = sqrt(np.mean(np.square(diff)))
    return mse
