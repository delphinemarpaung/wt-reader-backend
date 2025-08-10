import os
import pinyin
from const import CHAPTER
import pyttsx3
from src.components.file_utils import get_image_file_ls_from_html
from src.app.const import IS_MAC_OS


def get_text_from_image(filepath):
    if IS_MAC_OS:
        from src.components.text_extractor_macos import text_from_image
        texts, _ = text_from_image(image=filepath, recognition_level="accurate", language_preference=["zh-Hant"],
                                   confidence_threshold=0.01, text_group=False)
    else:
        from src.components.text_extractor import text_from_image
        texts = text_from_image(image=filepath, language_preference='chi_tra')
    return texts


def batch_process_images():
    chapter_name = 'chapter{}'.format(CHAPTER)
    batch_file_fp = os.path.join("../resource/batch_files", "{}.txt".format(chapter_name))

    # get main html file and extract image filenames list
    image_tag_filenames = get_image_file_ls_from_html()

    print("processing image files")
    engine = pyttsx3.init()
    for img_id, image_filename in enumerate(image_tag_filenames):
        print("image file {} / {}".format(img_id + 1, len(image_tag_filenames)))
        filepath = "../resource/images/{}/{}".format(chapter_name, image_filename)
        if os.path.isfile(filepath):
            # get text
            texts = get_text_from_image(filepath)

            # get pinyin
            pinyins = [pinyin.get(text) for text in texts]

            # save to batch filepath: img id,img path,text id,text,pinyin,audio file path
            batch_fp_lines = []
            for text_id, text, text_pinyin in zip(range(len(texts)), texts, pinyins):
                batch_fp_lines.append("{},{},{},{},{},".format(img_id, filepath,
                                                               text_id, text, text_pinyin))
            with open(batch_file_fp, 'a') as f:
                f.write("\n".join(batch_fp_lines) + "\n")

    engine.stop()


if __name__ == '__main__':
    batch_process_images()
