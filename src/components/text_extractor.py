from typing import List
import pytesseract


def text_from_image(image, language_preference='chi_tra') -> List[str]:
    print(pytesseract.get_languages(config=''))
    original_text = pytesseract.image_to_string(image, lang=language_preference)
    texts = []
    for text in original_text.split("\n"):
        if len(text) > 0:
            texts.append(text)
    return texts
