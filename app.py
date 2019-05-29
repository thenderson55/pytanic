from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy  # connecting db like "knex"
# from flask_cors import CORS
import os 
import pandas as pd
import random
import numpy as py
from data import Articles
from models import create_passenger, get_passengers, delete_passenger, delete_all_passengers

pd.options.display.max_rows = 20
titanic = pd.read_csv('titanic.csv')


Articles = Articles()
app = Flask(__name__)
# CORS(app)


# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

outcomes = ["lol, no...", "Rose pushed you under..", "Jack sacraficed himself for you!", "Damn right- you swam to NY!", "Who cares!?", "A shark ate you..", "Well, you're here aren't you!?"]


@app.route("/")
def hello():
  return render_template("home.html")

@app.route("/titanic")
def titanic_info():
  return render_template("titanic.html", titanic = titanic, info = titanic.to_numpy()[400], tables=[titanic.to_html(classes='data')], titles=titanic.columns.values)

@app.route("/name/<name>")
def get_book_name(name):
  return f"name: {name}"

@app.route("/form", methods=['GET', 'POST', 'DELETE'])
def form():
  # return render_template('form.html')
  if request.method == 'GET':
    pass
  if request.method == 'POST':
    if request.form.get('id') == 'all':
      delete_all_passengers()
    elif request.form.get('id') != '':
      id = request.form.get('id')
      delete_passenger(id)
    else:
      print(request.form)
      name = request.form.get('name')
      age = request.form.get('age')
      sex = request.form.get('sex')
      pclass = request.form.get('pclass')
      fare = request.form.get('fare')
      # survived = request.form.get('survived')
      survived = random.choice(outcomes)
      # print(survived)
      create_passenger(name, age, sex, pclass, fare, survived)
    # delete_all_passengers()

  passengers = get_passengers()
  return render_template('form.html', passengers = passengers, outcome = random.choice(outcomes)
  )
  

@app.route("/articles")
def articles():
  return render_template('articles.html', articles = Articles)

@app.route("/article/<string:id>/")
def article(id):
  return render_template('article.html', title = Articles[int(float(id)) -1 ]["title"], description = Articles[int(float(id)) - 1]["description"])

@app.route("/details")
def get_book_details():
  author = request.args.get('author')
  published = request.args.get('published')
  return f"Author: {author}, Published: {published}"

if __name__ == '__main__':
  app.run(debug=True)