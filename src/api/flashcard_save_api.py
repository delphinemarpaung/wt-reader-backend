from flask_restful import Resource, request
from src.app.const import CHAPTER


class FlashcardSaveApiHandler(Resource):
    def get(self):
        return {'statusCode': 200}

    def post(self):
        data = request.get_json()
        if 'word' in data and 'meaning' in data:
            word = data['word']
            meaning = data['meaning']
            with open("../resource/flashcards{}.txt".format(CHAPTER), "a") as f:
                f.write("{},{}\n".format(word, meaning))
        return {'statusCode': 200}
