import imdb
import sqlite3
import requests
import os

movies = imdb.IMDb()
conn = sqlite3.connect("movies.db")
c = conn.cursor()

# c.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='Movies' ''')
# print(c.fetchone())
# c.execute('''DROP TABLE Movies''')
# if c.fetchone() is 'None':
#    c.execute('''CREATE TABLE Movies (ID INTEGER, Title TEXT, Year INTEGER, Genre TEXT, Director TEXT, Writer TEXT, Runtime INTEGER, 'Production Company' TEXT)''')

c.execute(
    '''CREATE TABLE IF NOT EXISTS Movies (ID INTEGER, Title TEXT, Year INTEGER, Genre TEXT, Director TEXT, Writer TEXT, Runtime INTEGER, 'Production Company' TEXT)''')

limit = 300
try:
    last_index = open('last_index.txt', 'r')
    index = int(last_index.read()) + 1
except FileNotFoundError as e:
    index = 1

counter = 0
while True:
    if requests.get("https://www.imdb.com/title/tt%s/" % str(index).zfill(7)).status_code == 404:
        print("Invalid index: %d \nCounter: %d\n" % (index, counter))
        index += 1
    else:
        movie_id = str(index).zfill(7)
        data = movies.get_movie(movie_id).data
        accepted = False
        if data['kind'] is 'movie' and ('United States' in data['countries'] if 'countries' in data else False):
                accepted = True
                movie = [index,

                         data['title'] if 'title' in data
                         else None,

                         data['year'] if 'year' in data
                         else None,

                         data['genres'][0] if 'genres' in data and type(data['genres']) is list
                         else data['genres'] if 'genres' in data
                         else None,

                         data['directors'][0].__str__() if 'directors' in data and type(data['directors']) is list
                         else data['directors'] if 'directors' in data
                         else None,

                         data['writers'][0].__str__() if 'writers' in data and type(data['writers']) is list
                         else data['writers'] if 'writers' in data
                         else None,

                         int(data['runtimes'][0]) if 'runtimes' in data and type(data['runtimes']) is list
                         else int(data['runtimes']) if 'runtimes' in data
                         else None,

                         data['production companies'][0].__str__() if 'production companies' in data and type(
                             data['production companies']) is list
                         else data['production companies'] if 'production companies' in data
                         else None]

                c.execute('''INSERT INTO Movies VALUES (?,?,?,?,?,?,?,?)''', movie)
                counter += 1
                print("Accepted index: %d \nCounter: %d\n" % (index, counter))
                if counter >= limit:
                    with open('last_index.txt', 'w') as file:
                        file.write(str(index))
                    break
        if not accepted:
            print("Rejected index: %d \nCounter: %d\n" % (index, counter))
        index += 1

conn.commit()
conn.close()
