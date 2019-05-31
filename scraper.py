from bs4 import BeautifulSoup
import requests
import pandas as pd 
import re
from urllib.request import urlopen, Request
import random


cc_students = []
cc_names = []
cc_links = []
cc_talks = []
cc_pages = []
cc_images = []
cc_titanic = []

outcomes = ["lol, no...", "Rose pushed you under..", "Jack sacraficed himself for you!", "Damn right- you swam to NY!", "Who cares!?", "A shark ate you..", "Well, you're here aren't you!?"]
for i in range(0, 27):
  survived = random.choice(outcomes)
  cc_titanic.append(survived)
print(cc_titanic)

for i in range(4, 8):
  cc_pages.append(f'https://codechrysalis.io/cc{i}')

print(cc_pages)

for page in cc_pages:
  source = requests.get(page).text
  soup = BeautifulSoup(source, 'lxml')
  # images = soup.find_all('img', {'src':re.compile('.jpg')})

  for student in soup.find_all(class_='student-graduate'):
    cc_students.append(student)

  for image in soup.find_all('img', {'src':re.compile('.jpg')}):
    cc_images.append(image['src'])

  # counter = 0
  # for img in soup.find_all('img'):
  #   with open("image" + str(counter),'wb') as f:
  #       f.write(urlopen(img['src']).read())
  #   counter += 1

  for name in soup.find_all(class_='student-graduate__name'):
    cc_names.append(name.text)

  for link in soup.find_all(class_="student-profile__github-link"):
    cc_links.append(link["href"])

  for talk in soup.find_all(class_="student-profile__deploy-link"):
    cc_talks.append(talk["href"])

git_links = []
in_links = []
cv_links = []
print(len(cc_images))

for i in range(0, 81, 3):
  git_links.append(cc_links[i])

for i in range(1, 81, 3):
  in_links.append(cc_links[i])

for i in range(2, 81, 3):
  cv_links.append(cc_links[i])
  

data = {'Name': cc_names,
        'Github': git_links,
        'Linkedin': in_links,
        'CV': cv_links,
        'Titanic?': cc_titanic
        }

df = pd.DataFrame(data)
df.to_csv("/Users/admin/Desktop/py-course/titanic/cc-tables.csv")

# with open('simple.html') as html_file:

# with open('https://codechrysalis.io/cc4') as html_file:
#   ccstudents = BeautifulSoup(html_file, 'lxml')
# name = ccstudents.find(class_='student-graduate__name')
# print(name.text)

# yolo = soup.find_all('h3', class_='heading')
