import requests
from operator import itemgetter


DIFFICULTY = ("easy", "medium", "hard")
MAX_QUESTIONS = 50


class ApiClient:
    CATEGORIES_URL = "https://opentdb.com/api_category.php"
    QUESTIONS_URL_WITH_DIFFICULTY = "https://opentdb.com/api.php?amount={}&category={}&difficulty={}"
    QUESTIONS_URL_WITHOUT_DIFFICULTY = "https://opentdb.com/api.php?amount={}&category={}"
    QUESTIONS_COUNT_FOR_CATEGORY = "https://opentdb.com/api_count.php?category={}"

    @classmethod
    def get_quiz_options(cls):
        '''
        Returns dictionary with options to select for user.
        '''
        result = {"categories": requests.get(ApiClient.CATEGORIES_URL).json()["trivia_categories"], 
                "max_questions": MAX_QUESTIONS, "difficulty": DIFFICULTY}
        return result

    @classmethod
    def get_questions(cls, number_of_questions, category, difficulty):
        '''
        Returns dictionary with questions based on provided options by user from OpenTriviaDB.
        '''
        total_question_count, total_easy_question_count, total_medium_question_count, total_hard_question_count = itemgetter(
            'total_question_count',
            'total_easy_question_count',
            'total_medium_question_count',
            'total_hard_question_count'
        )(requests.get(ApiClient.QUESTIONS_COUNT_FOR_CATEGORY.format(category)).json()['category_question_count'])

        if int(number_of_questions) >= total_question_count:
            # if requested number of questions is higher than total count of questions in API then returns total available
            # questions from API
            results = requests.get(ApiClient.QUESTIONS_URL_WITHOUT_DIFFICULTY.format(total_question_count, category)).json()['results']
        else:
            results = requests.get(ApiClient.QUESTIONS_URL_WITH_DIFFICULTY.format(number_of_questions, category, difficulty)).json()['results']
            if not results:
                # If requested number of questions for a given category and difficulty is higher than total count for that category and difficulty
                # then load all available questions for that category with a requested category
                if difficulty == "easy":
                    results = requests.get(ApiClient.QUESTIONS_URL_WITH_DIFFICULTY.format(total_easy_question_count, category, difficulty)).json()['results']
                elif difficulty == "medium":
                    results = requests.get(ApiClient.QUESTIONS_URL_WITH_DIFFICULTY.format(total_medium_question_count, category, difficulty)).json()['results']
                elif difficulty == "hard":
                    results = requests.get(ApiClient.QUESTIONS_URL_WITH_DIFFICULTY.format(total_hard_question_count, category, difficulty)).json()['results']
        return results
