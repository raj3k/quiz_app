from sre_parse import CATEGORIES
from requests import get


DIFFICULTY = ("easy", "medium", "hard")
MAX_QUESTIONS = 50


class ApiClient:
    CATEGORIES_URL = "https://opentdb.com/api_category.php"
    QUESTIONS_URL = "https://opentdb.com/api.php?amount={}&category={}&difficulty={}"

    @classmethod
    def get_quiz_options(cls):
        result = {"categories": get(ApiClient.CATEGORIES_URL).json()["trivia_categories"], 
                "max_questions": MAX_QUESTIONS, "difficulty": DIFFICULTY}
        return result