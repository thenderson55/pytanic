from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy  # connecting db like "knex"
# from flask_cors import CORS
import requests
import json
import os 
import pandas as pd
import random
import numpy as py
from data import Articles
from models import create_passenger, get_passengers, delete_passenger, delete_all_passengers

pd.options.display.max_rows = 20
titanic = pd.read_csv('titanic.csv')
# titanic = titanic(r'\s+|\\n', ' ', regex=True, inplace=True) 


Articles = Articles()
app = Flask(__name__)
# CORS(app)


# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

outcomes = ["lol, no...", "Rose pushed you under..", "Jack sacraficed himself for you!", "Damn right- you swam to NY!", "Who cares!?", "A shark ate you..", "Well, you're here aren't you!?"]


@app.route("/")
def hello():
  beer_data = requests.get("https://api.punkapi.com/v2/beers")
  return render_template("home.html", beers=json.loads(beer_data.text))

@app.route("/titanic", methods=['GET', 'POST'])
def titanic_info():
  if request.method == "GET":
    print(request)
    print('hello')
    return render_template("titanic.html", titanic = titanic, tables=[titanic.to_html(classes='table')], titles=titanic.columns.values, show_average = False)

  if request.method == "POST":
    print(request.form)
    print('hello')
    if "averages-button" in request.form:
      average_choice = request.form.get('average')
      # data_choice = average_choice.capitalize()
      avg_data = titanic[average_choice].mean()
      desc = titanic.describe(include='all')
      return render_template("titanic.html", titanic = titanic, avg_data = avg_data, average_choice = average_choice, tables=[titanic.to_html(classes='table')], titles=titanic.columns.values, show_average = True)

    if "stats-button" in request.form:
      # tabel_choice = request.form.get('table')
      # st = titanic.strip()
      desc = titanic.describe(include='all')
      # desc.replace(r'\s+|\\n', ' ', regex=True, inplace=True) 
      # desc = desc.replace(r'\\n',' ', regex=True)
      print(desc)
      # desc = desc.replace(r'[\n\s]+', '')
      return render_template("titanic.html", titanic = titanic, tables=[titanic.to_html(classes='table')], titles=titanic.columns.values, show_stats = True, stat=[desc.to_html(classes='table')])

    if "all-data-button" in request.form: 
      if request.form.get('start') == '' and request.form.get('end') == '':
        return render_template("titanic.html", titanic = titanic, tables=[titanic.to_html(classes='table')], titles=titanic.columns.values)
      start = int(request.form.get('start'))
      if request.form.get('end'):
        end = int(request.form.get('end')) + 1
      else:
        end = start + 1
      return render_template("titanic.html", titanic = titanic[start:end], tables=[titanic[start:end].to_html(classes='table')], titles=titanic[start:end].columns.values)


@app.route("/name/<name>")
def get_book_name(name):
  return f"name: {name}"

@app.route("/form", methods=['GET', 'POST'])
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