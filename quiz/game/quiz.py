from dataclasses import dataclass, field
from random import shuffle
from typing import List

from quiz.api.client import ApiClient


@dataclass
class Question:
    category: str
    type: str
    difficulty: str
    question: str
    correct_answer: str
    incorrect_answers: List[str]
    answers: List[str] = field(default_factory=list, init=False)

    def check_answer(self, answer:str):
        return answer == self.correct_answer

    def __post_init__(self):
        self.answers.extend(self.incorrect_answers)
        self.answers.append(self.correct_answer)
        shuffle(self.answers)



@dataclass
class Quiz:
    number_of_questions: int
    difficulty: str
    questions: List[Question]
    current_question: int
    number_of_correct_answers: int

    @classmethod
    def create_game(cls, number_of_questions: int, difficulty: str, category: str):
        raw_questions = ApiClient.get_questions(difficulty, number_of_questions, category)
        questions = list([Question(**raw_question) for raw_question in raw_questions])
        return Quiz(number_of_questions, difficulty, questions, 0, 0)

    def save(self, request):
        request.session['saved_quiz'] = self

    def stop(self, request):
        del request.session['saved_quiz']

    @classmethod
    def restore(cls, request):
        return request.session.get('saved_quiz')