from flask_restful import Resource
from src.components.word_reminder import WordReminder
from src.app.const import CHAPTER


class FillBlankApiHandler(Resource):
    def __init__(self):
        self.word_reminder = WordReminder(is_fill_blank=True)

    def get(self):
        return {'statusCode': 200,
                'img_path_ls': [], 'word_ls': [], 'word_pinyin_ls': [],
                'meaning_ls': [], 'text_ls': [], 'pinyin_ls': []}

    def post(self):
        print("post")

        img_path_ls, word_ls, word_pinyin_ls, meaning_ls, text_ls, pinyin_ls = self.word_reminder.get_words()

        return {'statusCode': 200,
                'img_path_ls': img_path_ls, 'word_ls': word_ls, 'word_pinyin_ls': word_pinyin_ls,
                'meaning_ls': meaning_ls, 'text_ls': text_ls, 'pinyin_ls': pinyin_ls}
