from PIL import Image
import io
import objc
from typing import List, Tuple
from hanziconv import HanziConv
from src.components.text_grouping import get_text_group
import Vision


def pil2buf(pil_image: Image.Image):
    """Convert PIL image to buffer"""
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    return buffer.getvalue()


def text_from_image(
        image, recognition_level="accurate", language_preference=None, confidence_threshold=0.0,
        text_group=False
) -> Tuple[List[str], List[float]]:
    """
    Helper function to call VNRecognizeTextRequest from Apple's vision framework.

    :param image: Path to image (str) or PIL Image.Image.
    :param recognition_level: Recognition level. Defaults to 'accurate'.
    :param language_preference: Language preference. Defaults to None.
    :param confidence_threshold: Confidence threshold. Defaults to 0.0.
    :param text_group: apply text grouping based on bounding box if True

    :returns: List of tuples containing the text, the confidence and the bounding box.
        Each tuple looks like (text, confidence, (x, y, width, height))
        The bounding box (x, y, width, height) is composed of numbers between 0 and 1,
        that represent a percentage from total image (width, height) accordingly.
        You can use the `convert_coordinates_*` functions to convert them to pixels.
        For more info, see https://developer.apple.com/documentation/vision/vndetectedobjectobservation/2867227-boundingbox?language=objc
        and https://developer.apple.com/documentation/vision/vnrectangleobservation?language=objc
    """

    if isinstance(image, str):
        image = Image.open(image)
    elif not isinstance(image, Image.Image):
        raise ValueError("Invalid image format. Image must be a path or a PIL image.")

    if recognition_level not in {"accurate", "fast"}:
        raise ValueError(
            "Invalid recognition level. Recognition level must be 'accurate' or 'fast'."
        )

    if language_preference is not None and not isinstance(language_preference, list):
        raise ValueError(
            "Invalid language preference format. Language preference must be a list."
        )

    with objc.autorelease_pool():
        req = Vision.VNRecognizeTextRequest.alloc().init()

        if recognition_level == "fast":
            req.setRecognitionLevel_(1)
        else:
            req.setRecognitionLevel_(0)

        if language_preference is not None:

            available_languages = req.supportedRecognitionLanguagesAndReturnError_(None)[0]

            if not set(language_preference).issubset(set(available_languages)):
                raise ValueError(
                    f"Invalid language preference. Language preference must be a subset of {available_languages}."
                )
            req.setRecognitionLanguages_(language_preference)

        handler = Vision.VNImageRequestHandler.alloc().initWithData_options_(
            pil2buf(image), None
        )

        success = handler.performRequests_error_([req], None)
        texts, confidences, boxes = [], [], []
        if success:
            for result in req.results():
                if result.confidence() >= confidence_threshold:
                    texts.append(HanziConv.toSimplified(result.text()))
                    confidences.append(result.confidence())
                    box = result.boundingBox()
                    boxes.append([box.origin.x, box.origin.y, box.size.height, box.size.width])  # x, y, height, width

        if text_group:
            texts, confidences = get_text_group(texts, confidences, boxes)

        return texts, confidences


# if __name__ == '__main__':
#     import os
#
#     fp = "../resource/images/chapter0/1530265691173141110.jpg"
#     texts, _ = text_from_image(image=fp, recognition_level="accurate",
#                                language_preference=["zh-Hant"], confidence_threshold=0.01,
#                                text_group=True)
