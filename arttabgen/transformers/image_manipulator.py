"""Holds functions to process image manipulators on images.

IMAGE_MANIPULATORS: A list of all functions.
IMAGE_MANIPULATORS_BY_MODE: A mapping of table generation modes to image manipulators,
                            which can be used in each mode.
"""

from typing import Any, Callable, Dict, List

import cv2 as cv
import numpy as np
from PIL import Image


def process_image_blur(image: Image, value: int) -> Image.Image:
    """Apply a blur effect on an image.

    Args:
        image: Path of the image to be adjusted.
        value: Standard deviation in the X and Y directions. Must be > 0 and odd.

    Returns:
        The processed image.
    """

    img_raw = np.array(image)
    img_raw = cv.cvtColor(img_raw, cv.COLOR_RGB2BGR)
    # validation of `value` is done by OpenCV
    img_raw = cv.GaussianBlur(img_raw, (value, value), 0)

    return Image.fromarray(img_raw)


def process_image_contrast(image: Image, value: float) -> Image.Image:
    """Apply a contrast change to an image.

    Args:
        image: Path of the image to be adjusted.
        value: A number acting as ``alpha`` to scales each pixel's value, per channel:
               ``new_pixel_value = abs(pixel_value * alpha + beta)`` where ``beta = 0``.

    Returns:
        The processed image.
    """

    img_raw = np.array(image)
    img_raw = cv.cvtColor(img_raw, cv.COLOR_RGB2BGR)
    img_raw = cv.convertScaleAbs(img_raw, alpha=value, beta=0)

    return Image.fromarray(img_raw)


def process_image_brightness(image: Image, value: int) -> Image.Image:
    """Apply a brightness change to an image.

    Args:
        image: Path of the image to be adjusted.
        value: A number acting as ``beta`` to increase/decrease each pixel's value, per channel:
               ``new_pixel_value = abs(pixel_value * alpha + beta)`` where ``alpha = 1``.

    Returns:
        The processed image.
    """

    img_raw = np.array(image)
    img_raw = cv.cvtColor(img_raw, cv.COLOR_RGB2BGR)
    img_raw = cv.convertScaleAbs(img_raw, alpha=1, beta=value)

    return Image.fromarray(img_raw)


def process_image_noise(image: Image, value: float) -> Image.Image:
    """Apply a noise effect on an image.

    Args:
        image: Path of the image to be adjusted
        value: Probability.

    Returns:
        The processed image.
    """

    img_raw = np.asarray(image)
    img_raw = cv.cvtColor(img_raw, cv.COLOR_RGB2BGR)

    img_raw = _add_sp_noise(img_raw, value)

    return Image.fromarray(img_raw)


def process_image_sharpness(image: Image) -> Image.Image:
    """Apply a sharpness change to an image.

    Args:
        image: Path of the image to be adjusted.

    Returns:
        The processed image.
    """

    img_raw = np.array(image)
    img_raw = cv.cvtColor(img_raw, cv.COLOR_RGB2BGR)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    img_raw = cv.filter2D(src=img_raw, ddepth=-1, kernel=kernel)

    return Image.fromarray(img_raw)


def _add_sp_noise(img_raw: np.array, prob: float) -> np.array:
    """Apply salt and pepper noise to an image.

    https://gist.github.com/lucaswiman/1e877a164a69f78694f845eab45c381a

    Args:
        img_raw: Path of the image to be adjusted.
        prob: Probability of a pixel being altered.

    Returns:
        An Image with salt and pepper noise applied.

    """
    if len(img_raw.shape) == 2:
        black = 0
        white = 255
    else:
        colorspace = img_raw.shape[2]

        if colorspace == 3:  # RGB
            black = np.array([0, 0, 0], dtype="uint8")
            white = np.array([255, 255, 255], dtype="uint8")
        else:  # RGBA
            black = np.array([0, 0, 0, 255], dtype="uint8")
            white = np.array([255, 255, 255, 255], dtype="uint8")
    probs = np.random.random(img_raw.shape[:2])
    img_raw[probs < (prob / 2)] = black
    img_raw[probs > 1 - (prob / 2)] = white

    return img_raw


IMAGE_MANIPULATORS: Dict[str, Callable[[Any, Any], Image.Image]] = {
    "blur": process_image_blur,
    "contrast": process_image_contrast,
    "brightness": process_image_brightness,
    "sharpness": process_image_sharpness,
    "noise": process_image_noise,
}
"""Holds all defined image manipulators."""

IMAGE_MANIPULATORS_BY_MODE: Dict[int, List[str]] = {
    1: ["sharpness"],
    2: ["contrast", "brightness", "sharpness"],
    3: ["blur", "contrast", "brightness", "sharpness"],
    4: ["blur", "contrast", "brightness", "sharpness", "noise"],
}
"""Maps table generation modes to the image manipulators, which can be used in that mode."""
