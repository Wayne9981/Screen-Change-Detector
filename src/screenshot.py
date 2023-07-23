import logging
import os
from collections import deque
from math import sqrt
from datetime import datetime
from functools import cached_property


import mss
from PIL import ImageChops, Image
import numpy as np

from utils import log_times

logger = logging.getLogger(__name__)
queue = deque(maxlen=2)


class ScreenshotProxy:
    @cached_property
    def sct(self):
        return mss.mss()

    @staticmethod
    @log_times
    def compare_images(img1: Image, img2: Image) -> float:
        diff_image = ImageChops.difference(img1, img2)
        diff = np.asarray(diff_image, dtype=np.half) / 255  # type: ignore
        mse = sqrt(np.mean(np.square(diff)))
        return mse
    
    @log_times
    def screen_analysis(self, diff_threshold_percentage: int, image_folder: str, box: list[int]):
        img = self.sct.grab(tuple(box))
        img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        queue.append(img)
        if len(queue) > 1:
            diff = self.compare_images(queue[0], queue[1])
            logger.info(f"{diff = :.2%}")
            print(f"diff: {diff:.2%}")
            if diff > diff_threshold_percentage / 100:
                os.makedirs(image_folder, exist_ok=True)
                file_path = f"{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.jpeg"
                logging.info(f"{file_path = }")
                print(f"Saved image: {file_path}")
                mss.tools.to_png(img.rgb, img.size, output=os.path.join(image_folder, file_path))

