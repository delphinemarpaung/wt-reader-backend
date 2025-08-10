import jieba
from cihai.core import Cihai
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from hanziconv import HanziConv
import pinyin


class TextAnalyser:
    """
    - For a given text in Traditional chinese,
        return the English translation, list of words, and list of pinyins
    - This analyzer use cihai and cedict vocabulary, and Helsinki-NLP translation model
    """
    def __init__(self, filename: str = '../dictionary/cedict_ts.u8', enable_translation: bool = True):
        # load cihai vocab
        self.cihai = Cihai()
        if not self.cihai.unihan.is_bootstrapped:  # download and install Unihan to db
            self.cihai.unihan.bootstrap()

        # load cedict vocab
        self.cedict_zh_dct = {}
        self._init_cedict_vocabs(filename)

        # load translation model
        self.enable_translation = enable_translation
        self.tokenizer, self.model = None, None
        if self.enable_translation:
            self.tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
            self.model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-zh-en")

    def _init_cedict_vocabs(self, filename):
        with open(filename) as file:
            for line in file.read().split('\n'):
                if line == '' or line.startswith('#'):
                    continue

                line_part = line.rstrip('/').split('/')
                if len(line_part) <= 1:
                    continue

                english = line_part[1]
                char_and_pinyin = line_part[0].split('[')

                characters = char_and_pinyin[0].split()
                traditional = characters[0]
                simplified = characters[1]

                pinyin = char_and_pinyin[1].rstrip().rstrip("]")

                self.cedict_zh_dct[simplified] = {
                    'traditional': traditional,
                    'pinyin': pinyin,
                    'english': english
                }

    def _get_cihai_word_translation(self, words):
        cihai_words = {}
        for word in words:
            query = self.cihai.unihan.lookup_char(word)
            glyph = query.first()
            if glyph is not None:
                cihai_words[word] = glyph.kDefinition
        return cihai_words

    def _get_cedict_word_translation(self, words):
        cedict_words = {}
        for word in words:
            if word in self.cedict_zh_dct:
                cedict_words[word] = self.cedict_zh_dct[word]
        return cedict_words

    def _get_word_translation(self, text: str):
        words = list(jieba.cut(text, cut_all=False))
        cihai_words = self._get_cihai_word_translation(words)
        cedict_words = self._get_cedict_word_translation(words)
        return cihai_words, cedict_words, words

    def _get_sentence_translation(self, text: str):
        input_ids = self.tokenizer.encode(text, return_tensors="pt")
        outputs = self.model.generate(input_ids)
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return str(decoded)

    def analyze(self, text: str, is_debug: bool = False):
        # convert to simplified chinese
        text = HanziConv.toSimplified(text)

        # get translation
        if self.enable_translation:
            translation = self._get_sentence_translation(text)
        else:
            translation = ""
        if is_debug:
            print("Translation: {}\nVocabs:".format(translation))

        # get list of word, pinyin, and meaning
        cihai_words, cedict_words, original_words = self._get_word_translation(text)
        words = []
        for word in original_words:
            if word in cedict_words:
                detail = cedict_words[word]
                words.append({
                    'word': word,
                    'pinyin': detail['pinyin'],
                    'meaning': detail['english']})
                if is_debug:
                    print("word: {}, pinyin: {}, translation: {}".format(
                        word, detail['pinyin'], detail['english']))
            elif word in cihai_words:
                detail = cihai_words[word]
                words.append({
                    'word': word,
                    'pinyin': pinyin.get(word),
                    'meaning': detail})
                if is_debug:
                    print("word: {}, pinyin: {}, translation: {}".format(word, pinyin.get(word), detail))
            else:
                words.append({
                    'word': word,
                    'pinyin': pinyin.get(word),
                    'meaning': ''})

        return translation, words, text


# if __name__ == '__main__':
#     analyzer = TextAnalyser()
#     analyzer.analyze(text="中国加快开采绿色技术所需金属 但在多国引发焦虑", is_debug=True)
