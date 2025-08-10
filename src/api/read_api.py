from flask_restful import Resource
import os
from src.components.file_utils import get_image_file_ls_from_html, read_batch_file
from src.app.const import CHAPTER


CHAPTER_NAME = 'chapter{}'.format(CHAPTER)


class ReadApiHandler(Resource):
    def __init__(self):
        self.image_filenames = []
        self.texts_ls = []
        self.pinyin_ls = []
        self.audio_ls = []

        # get main html file and extract image filenames list
        image_tag_filenames = get_image_file_ls_from_html()

        # read batch file
        image_dct = read_batch_file()

        # get list of texts
        for filename in image_tag_filenames:
            filepath = "../resource/images/{}/{}".format(CHAPTER_NAME, filename)
            if os.path.isfile(filepath):
                self.image_filenames.append(filename)
                image_details = image_dct.get(filepath, {})
                self.texts_ls.append(image_details.get('text', []))
                self.pinyin_ls.append(image_details.get('text_pinyin', []))
                self.audio_ls.append(image_details.get('audio_file', []))

    def get(self):
        return {'statusCode': 200, 'image_filenames': [], 'texts_ls': [], 'pinyin_ls': [], 'audio_ls': []}

    def post(self):
        return {
            'statusCode': 200,
            'image_filenames': self.image_filenames,
            'texts_ls': self.texts_ls,
            'pinyin_ls': self.pinyin_ls,
            'audio_ls': self.audio_ls
        }
