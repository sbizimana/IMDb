import imdb
import sqlite3
import requests

movies = imdb.IMDb()
conn = sqlite3.connect("movies.db")
c = conn.cursor()

c.execute('''DROP TABLE Performers''')
c.execute('''DROP TABLE Films''')
c.execute('''DROP TABLE Directors''')
c.execute('''DROP TABLE MoviesData''')
c.execute('''CREATE TABLE IF NOT EXISTS Performers (CharacterID TEXT, Name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS Films (MovieID TEXT, Title TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS Directors (DirectorID TEXT, Name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS MoviesData (MovieID TEXT, CharacterID TEXT, Year INTEGER, Genre TEXT, DirectorID TEXT)''')

limit = 3
try:
    last_index = open('last_index1m.txt', 'r')
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
        is_film = data['kind'] is 'movie'
        has_title = 'title' in data
        has_cast = 'cast' in data
        has_director = 'directors' in data
        has_genre = 'genres' in data
        in_usa = 'United States' in data['countries'] if 'countries' in data else False
        if is_film and has_title and has_cast and has_director and has_genre and in_usa:
            accepted = True

            performers = [[data['cast'][x].getID(), data['cast'][x].__str__()] for x in range(len(data['cast']))]
            for performer in performers:
                c.execute('''INSERT INTO Performers VALUES (?,?)''', performer)
            c.execute('''CREATE TABLE temp AS SELECT DISTINCT * FROM Performers''')
            c.execute('''DROP TABLE Performers''')
            c.execute('''CREATE TABLE Performers AS SELECT * FROM temp''')
            c.execute('''DROP TABLE temp''')

            movie = [movie_id, data['title']]
            c.execute('''INSERT INTO Films VALUES (?,?)''', movie)

            directors = [[data['directors'][x].getID(), data['directors'][x].__str__()] for x in range(len(data['directors']))]
            c.execute('''SELECT DirectorID FROM Directors''')

            for director in directors:
                c.execute('''INSERT INTO Directors VALUES (?,?)''', director)
            c.execute('''CREATE TABLE temp AS SELECT DISTINCT * FROM Directors''')
            c.execute('''DROP TABLE Directors''')
            c.execute('''CREATE TABLE Directors AS SELECT * FROM temp''')
            c.execute('''DROP TABLE temp''')

            for x in range(len(data['cast'])):
                for y in range(len(data['directors'])):
                    c.execute('''INSERT INTO MoviesData VALUES (?,?,?,?,?)''', [movie_id,
                                                                                data['cast'][x].getID(),
                                                                                data['year'],
                                                                                data['genres'][0],
                                                                                data['directors'][y].getID()])

            counter += 1
            print("Accepted index: %d \nCounter: %d\n" % (index, counter))
            if counter >= limit:
                with open('last_index1.txt', 'w') as file:
                    file.write(str(index))
                break
    if not accepted:
        print("Rejected index: %d \nCounter: %d\n" % (index, counter))
    index += 1

conn.commit()
conn.close()
