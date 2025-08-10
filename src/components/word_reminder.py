import pinyin
from src.components.file_utils import get_image_file_ls_from_html, read_batch_file
from src.app.const import CHAPTER


class WordReminder:
    def __init__(self, is_fill_blank=False):
        self.img_path_ls = []
        self.text_ls = []
        self.pinyin_ls = []

        # read flashcards
        self.word_ls, self.word_pinyin_ls, self.meaning_ls = [], [], []
        flash_cards_fp = "../resource/flashcards{}.txt".format(CHAPTER)
        self._read_flash_cards(flash_cards_fp)

        # extract image filenames list from html file
        image_filenames = get_image_file_ls_from_html()

        # get list of images and texts from batch file
        image_dct = read_batch_file()

        # get the related image file for each word in flashcard
        word2imgidx_dct, image_texts, image_pinyins = self._find_word_in_image_files(
            image_filenames=image_filenames, image_dct=image_dct)

        # get word2text
        to_remove_idx = []
        for i, word in enumerate(self.word_ls):
            # if flash card word not found
            if word not in word2imgidx_dct:
                to_remove_idx.append(i)
                continue

            # get processed text related to that word
            img_idx = word2imgidx_dct[word]
            self.img_path_ls.append(image_filenames[img_idx])
            if is_fill_blank:
                processed_texts, processed_pinyins = self._hide_word_in_text(
                    word=word, texts=image_texts[img_idx], pinyins=image_pinyins[img_idx])
            else:
                processed_texts, processed_pinyins = self._highlight_word_in_text(
                    word=word, texts=image_texts[img_idx], pinyins=image_pinyins[img_idx])
            self.text_ls.append(processed_texts)
            self.pinyin_ls.append(processed_pinyins)

        # remove flashcard words that are not found in image files
        for i in to_remove_idx[::-1]:
            self.word_ls.pop(i)
            self.word_pinyin_ls.pop(i)
            self.meaning_ls.pop(i)

    def _find_word_in_image_files(self, image_filenames, image_dct):
        """ For each word in self.word_ls, find the related image filename index, text, and pinyin. """
        unprocessed_words = set(self.word_ls)
        word2imgidx_dct = {}
        image_texts, image_pinyins = [], []
        for i, filename in enumerate(image_filenames):
            filepath = "../resource/images/chapter{}/{}".format(CHAPTER, filename)
            image_details = image_dct.get(filepath, {})
            texts = image_details.get('text', [])
            pinyins = image_details.get('text_pinyin', [])
            for text in texts:
                # check if text contain words
                found_words = []
                for word in unprocessed_words:
                    if word in text:
                        word2imgidx_dct[word] = i
                        found_words.append(word)
                for word in found_words:
                    unprocessed_words.remove(word)

            image_texts.append(texts)
            image_pinyins.append(pinyins)
        return word2imgidx_dct, image_texts, image_pinyins

    def _read_flash_cards(self, flash_cards_fp):
        """ Extract word list from flash card file. """
        with open(flash_cards_fp, 'r') as f:
            for text in f.read().splitlines():
                if len(text) > 0:
                    text_comps = text.split(',')
                    word_pinyin_split = text_comps[0][:-1].split(" (")
                    word = word_pinyin_split[0]
                    word_pinyin = word_pinyin_split[-1]
                    meaning = text_comps[-1]
                    self.word_ls.append(word)
                    self.word_pinyin_ls.append(word_pinyin)
                    self.meaning_ls.append(meaning)

    @staticmethod
    def _highlight_word_in_text(word, texts, pinyins):
        processed_texts, processed_pinyins = [], []
        for text_pinyin, text in zip(pinyins, texts):
            if word in text:
                text_splits = text.split(word)
                processed_texts.append(f"<<{word}>>".join(text.split(word)))
                processed_pinyins.append(f"<<{pinyin.get(word)}>>".join([pinyin.get(s) for s in text_splits]))
            else:
                processed_texts.append(text)
                processed_pinyins.append(text_pinyin)
        return processed_texts, processed_pinyins

    @staticmethod
    def _hide_word_in_text(word, texts, pinyins):
        processed_texts, processed_pinyins = [], []
        for text_pinyin, text in zip(pinyins, texts):
            if word in text:
                text_splits = text.split(word)
                processed_texts.append("<<...>>".join(text_splits))
                processed_pinyins.append("<<...>>".join([pinyin.get(s) for s in text_splits]))
            else:
                processed_texts.append(text)
                processed_pinyins.append(text_pinyin)
        return processed_texts, processed_pinyins

    def get_words(self):
        return self.img_path_ls, self.word_ls, self.word_pinyin_ls, self.meaning_ls, self.text_ls, self.pinyin_ls


# if __name__ == '__main__':
#     word_reminder = WordReminder()
#     word_reminder.get_words()
#     print("done")
