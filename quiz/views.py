from django.shortcuts import redirect, render

from quiz.game.quiz import Quiz
from .api import ApiClient


def index(request):
    try:
        quiz = ApiClient.get_quiz_options()
        return render(request, "quiz/index.html", quiz)
    except ValueError:
        return render(request, "quiz/error.html")


def start_game(request):
    number_of_questions = request.POST['quantity']
    difficulty = request.POST['difficulty']
    category = request.POST['category']
    quiz = Quiz.create_game(number_of_questions, difficulty, category)
    quiz.save(request)
    return redirect('/on_game')


def on_game(request):
    quiz = Quiz.restore(request)

    if not quiz:
        return render(request, 'quiz/error.html')
    
    answer = request.POST.get('answer')

    if answer:
        quiz.just_started = False
        quiz.check_answer(answer)

    try:
        question = quiz.get_question()
        quiz.save(request)
        return render(request, 'quiz/game.html', vars(question))
    except IndexError as e:
        return redirect('/finish')


def finish(request):
    quiz = Quiz.restore(request)
    try:
        result = quiz.get_result()
        quiz.stop(request)
    except AttributeError as e:
        result = {}
    return render(request, 'quiz/finish.html', result)


