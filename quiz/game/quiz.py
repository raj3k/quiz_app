from dataclasses import dataclass, field
from random import shuffle
from typing import List
from html import unescape

from quiz.api.client import ApiClient
from django.core.handlers.wsgi import WSGIRequest


@dataclass
class Question:
    '''
    Question class to represent single question loaded from OpenTriviaDB.
    
    Attributes
    ----------
    category : str
        category of the question selected by user
    type : str
        type can be multiple or True/False
    difficulty : str
        difficulty of the question chosen by user ('easy', 'medium', 'hard')
    question : str
        the content of the question
    correct_answer : str
        correct answer for the given question
    incorrect_answers : List[str]
        list of incorrect answers for the gievn question
    answers : List[str]
        list of all answers for the given question. Created in __post_init__() method.
    '''
    category: str
    type: str
    difficulty: str
    question: str
    correct_answer: str
    incorrect_answers: List[str]
    answers: List[str] = field(default_factory=list, init=False)

    def check_answer(self, answer: str):
        '''
        Checks whether a selected answer is correct or not and returns Boolean value
        '''
        return answer == self.correct_answer

    def __post_init__(self) -> None:
        '''
        Method (called in __init__()) to:
        - replace special characters in questions and answers
        - assign all answers to list
        - shuffle list of answers
        '''
        self.question = unescape(self.question)
        self.answers.extend(self.incorrect_answers)
        self.answers.append(self.correct_answer)
        self.answers = [unescape(answer) for answer in self.answers]
        shuffle(self.answers)


@dataclass
class Quiz:
    '''
    A class to represent a Quiz game.

    Attributes
    ----------
    number_of_questions : int
        number of questions requested by user
    difficulty : str
        difficulty of the Quiz game ('easy', 'medium', 'hard')
    questions : List[Question]
        List containing objects of class Question
    number_of_correct_answers: int
        number of correct answers selected by user
    current_question : int
        number of currently displayed question to user
    just_started : bool
        flag variable to prevent from loading random questions on the page with
        question
    '''
    number_of_questions: int
    difficulty: str
    questions: List[Question]
    number_of_correct_answers: int
    current_question: int
    just_started: bool = field(default=True)

    @classmethod
    def create_game(cls, number_of_questions: int, difficulty: str, category: str):
        '''
        Returns a Quiz object.
        ----------------------
        Questions are being loaded by ApiClient.get_questions method from OpenTriviaDB.
        List of Question objects is created from loaded dictionary with questions.
        Returns a Quiz object with provided options.
        '''
        raw_questions = ApiClient.get_questions(number_of_questions, category ,difficulty)
        questions = list([Question(**raw_question) for raw_question in raw_questions])
        return Quiz(number_of_questions, difficulty, questions, 0, 0)

    def save(self, request: WSGIRequest) -> None:
        '''Saves current state of Quiz game in Session'''
        request.session['saved_quiz'] = self

    def stop(self, request: WSGIRequest) -> None:
        '''Removes Quiz game from Session'''
        del request.session['saved_quiz']

    @classmethod
    def restore(cls, request: WSGIRequest):
        '''Returns the state of current game of Quiz from Session'''
        return request.session.get('saved_quiz')

    def check_answer(self, answer: str):
        '''
        Checks if provided answer is correct for the given question and increments
        number_of_correct_answers if True.
        '''
        if self.questions[self.current_question - 1].correct_answer == answer:
            self.number_of_correct_answers += 1

    def get_result(self) -> dict:
        '''
        Returns the results of the game (correct_answers and number of all questions)
        '''
        return {
            'correct_answers': self.number_of_correct_answers,
            'all_questions': len(self.questions)
        }

    def get_question(self) -> Question:
        '''
        Returns single question from the list of questions (self.questions)
        and also increment current_question to prevent loading the same question again.

        Method also checks state of just_started flag which prevents from loading all questions
        on first question page by clicking F5 button (reload page).
        '''
        question = self.questions[self.current_question]
        if self.just_started:
            question = self.questions[0]
            self.current_question = 1
        else:
            question = self.questions[self.current_question]
            self.current_question += 1
        return question