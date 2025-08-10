from flask import Flask
from flask_restful import Api
from src.api.analyse_api import AnalyseApiHandler
from src.api.read_api import ReadApiHandler
from src.api.flashcard_save_api import FlashcardSaveApiHandler
from src.api.flashcard_api import FlashcardApiHandler
from src.api.word_reminder_api import WordReminderApiHandler
from src.api.fill_blank_api import FillBlankApiHandler
from flask_cors import CORS  # comment this on deployment


app = Flask(__name__)
app.config["SECRET_KEY"] = "hardkey"
CORS(app)  # comment this on deployment
api = Api(app)


@app.route('/')
def index():
    return "Welcome to mock app!"


# Main API for reading
api.add_resource(AnalyseApiHandler, '/analyse')
api.add_resource(ReadApiHandler, '/read')
api.add_resource(FlashcardSaveApiHandler, '/save')
api.add_resource(FlashcardApiHandler, '/flashcard')
api.add_resource(WordReminderApiHandler, '/reminder')
api.add_resource(FillBlankApiHandler, '/fillblank')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
