import imdb
import sqlite3
import requests

movies = imdb.IMDb()
conn = sqlite3.connect("movies.db")
c = conn.cursor()

c.execute('''DROP TABLE Movies''')
c.execute('''CREATE TABLE Movies
             (Title TEXT, Year INTEGER, Genre TEXT, Director TEXT, Writer TEXT, 'Runtime (minutes)' INTEGER, 'Production Company' TEXT)''')

limit = 1
x = 1
while True:

    request = requests.get("https://www.imdb.com/title/tt%s/" % str(x).zfill(7))

    if request.status_code == 404:
        print("Invalid Movie Link: https://www.imdb.com/title/tt%s/" % str(x).zfill(7))
    else:
        data = movies.get_movie(str(x).zfill(7740355)).data

        if data['kind'] is 'movie':
            movie = [data['title'],

                     data['year'],

                     data['genres'][0] if 'genres' in data and type(data['genres']) is list
                     else data['genres'] if 'genres' in data
                     else 'N/A',

                     data['directors'][0].__str__() if 'directors' in data and type(data['directors']) is list
                     else data['directors'] if 'directors' in data
                     else 'N/A',

                     data['writers'][0].__str__() if 'writers' in data and type(data['writers']) is list
                     else data['writers'] if 'writers' in data
                     else 'N/A',

                     int(data['runtimes'][0]) if 'runtimes' in data and type(data['runtimes']) is list
                     else int(data['runtimes']) if 'runtimes' in data
                     else -1,

                     data['production companies'][0].__str__() if 'production companies' in data and type(
                         data['production companies']) is list
                     else data['production companies'] if 'production companies' in data
                     else 'N/A']

            c.execute('''INSERT INTO Movies VALUES (?,?,?,?,?,?,?)''', movie)
            print(x)
    if x >= limit:
        break
    x += 1

conn.commit()
conn.close()
