from flask_restful import Resource, request
from src.components.text_analyser import TextAnalyser


class AnalyseApiHandler(Resource):
    def __init__(self):
        self.text_analyser = TextAnalyser()

    def get(self):
        return {'statusCode': 200, 'translation': "", 'words': [], 'text': ""}

    def post(self):
        data = request.get_json()
        if 'text' in data:
            text = data['text']
            translation, words, text = self.text_analyser.analyze(text)
            return {'statusCode': 200, 'translation': translation, 'words': words, 'text': text}
        else:
            return {'statusCode': 200, 'translation': "", 'words': [], 'text': ""}
