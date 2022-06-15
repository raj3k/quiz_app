# Quizzer
<h3>Project Description</h3>
<p>The goal for this project is to create web app that will allow users to play the Quiz game. User selects the amount of questions, difficulty and categorty for the questions. Based on that application generates set of questions for user. Each question is displayed to user one by one. After answering them, the game is over and the player sees his score.</p>

<h3>Technologies used</h3>
<ul>
  <li>Python version 3.10</li>
  <li>Django version 4</li>
  <li>Bootstrap version 5.2</li>
</ul>

<h3>Challenges faced:</h3>
<ul>
  <li>figuring out how to save user progress - resolved by saving and retriving progress from session</li>
  <li>numbers of questions - for example user selects 10 easy questions from Art category but API have only 9 of them and sending request for 10 is returning response code 1 with empty list (API documentation: <b>Code 1: No Results</b> Could not return results. The API doesn't have enough questions for your query. (Ex. Asking for 50 Questions in a Category that only has 20.). Solved by returning the amount of questions that currently API have.</li>
  <li>F5 issue on first question - clicking F5 on first question will load new question every time. To resolve this I used flag variable</li>
  <li>and few other minor challanges/issues</li>
</ul>

\### <h3>Features planned to implement:</h3>
- [ ] Current number of question (progress bar using Bootstrap library) -> currently working on that
- [ ] time cap for question
- [ ] limited hints in quiz
- [ ] Documentation
- [ ] Ranking

<h3>How to run application</h3>
<ol>
  <li>Clone repo</li>
  <li>Enter project: <b>cd quiz_app/ </b></li>
  <li>Create virtualenv: <b>python3 -m venv venv </b></li>
  <li>Install requirements: <b>pip3 install -r requirements.txt </b></li>
  <li>Source the virtual enviroment: <b>source venv/bin/activate</b></li>
  <li>Run django application: <b>python3 manage.py runserver</b> Note: There is no need to migrate db yet.</li>
</ol>

<h3>How to run application using docker</h3>
<ol>
  <li>Clone repo</li>
  <li>Enter project: <b>cd quiz_app/ </b></li>
  <li>Run command in terminal: <b>docker-compose up</b></li>
</ol>
