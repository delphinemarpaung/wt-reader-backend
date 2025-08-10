from flask_restful import Resource
from src.components.flash_card import FlashCard
from src.app.const import CHAPTER


class FlashcardApiHandler(Resource):
    def __init__(self):
        self.flash_card = FlashCard(flash_cards_fp="../resource/flashcards{}.txt".format(CHAPTER))

    def get(self):
        return {'statusCode': 200, 'question': "", 'option': [], 'answer': ""}

    def post(self):
        question, correct_answer, options = self.flash_card.run_flashcard()
        return {'statusCode': 200, 'question': question, 'options': options, 'answer': correct_answer}
