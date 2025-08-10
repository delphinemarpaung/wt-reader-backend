import random


class FlashCard:
    def __init__(self, flash_cards_fp):
        """ Read list of words from flash card file. """
        self.word2mean = {}
        self.mean2word = {}
        with open(flash_cards_fp, 'r') as f:
            for text in f.read().splitlines():
                if len(text) > 0:
                    text_comps = text.split(',')
                    word = text_comps[0]
                    meaning = text_comps[-1]
                    self.word2mean[word] = meaning
                    self.mean2word[meaning] = word

    def run_flashcard(self):
        """ Get random word and meaning, and sample 4 others words. """
        opt = random.randint(0, 1)
        if opt == 0:
            # flashcard1: zh word -> meaning, pinyin
            options = random.sample(list(self.mean2word.keys()), 4)
            correct_answer = random.choice(options)
            word = self.mean2word[correct_answer]
            question = "Meaning of {}?".format(word)
        else:
            # flashcard2: meaning -> zh word
            options = random.sample(list(self.word2mean.keys()), 4)
            correct_answer = random.choice(options)
            mean = self.word2mean[correct_answer]
            question = "Word for {}?".format(mean)

        return question, correct_answer, options
