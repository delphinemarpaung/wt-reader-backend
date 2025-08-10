from bs4 import BeautifulSoup
import re
import os
from src.app.const import CHAPTER


def get_image_file_ls_from_html():
    """ get main html file and extract image filenames list. """

    chapter_name = 'chapter{}'.format(CHAPTER)
    with open("../resource/images/{}.htm".format(chapter_name), 'r') as f:
        soup = BeautifulSoup(f.read(), features="lxml")
    image_tag_ls = soup.find_all('img', {'src': re.compile(r'\./{}_files/.*\.jpg'.format(chapter_name))})
    image_tag_filenames = []
    for image_tag in image_tag_ls:
        _, filename = os.path.split(image_tag['src'])
        image_tag_filenames.append(filename)

    return image_tag_filenames


def read_batch_file():
    """ Extract list of image files and the related text + pinyin + audio file. """
    batch_file_fp = os.path.join("../resource/batch_files", 'chapter{}.txt'.format(CHAPTER))
    lines = []
    if os.path.isfile(batch_file_fp):
        with open(batch_file_fp, 'r') as f:
            lines = f.read().splitlines()

    image_dct = {}
    for line in lines:
        if len(line.split(",")) != 6:
            continue
        _, filepath, _, text, text_pinyin, audio_file = line.split(",")
        if filepath not in image_dct:
            image_dct[filepath] = {'text': [], 'text_pinyin': [], 'audio_file': []}
        image_dct[filepath]['text'].append(text)
        image_dct[filepath]['text_pinyin'].append(text_pinyin)
        image_dct[filepath]['audio_file'].append(audio_file)

    return image_dct
