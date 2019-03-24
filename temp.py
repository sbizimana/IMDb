import imdb
import sqlite3
import requests

movies = imdb.IMDb()
conn = sqlite3.connect("movies2.db")
c = conn.cursor()

#c.execute('''DROP TABLE Performers''')
#c.execute('''DROP TABLE Films''')
#c.execute('''DROP TABLE Directors''')
#c.execute('''DROP TABLE MoviesData''')
c.execute('''CREATE TABLE IF NOT EXISTS Performers (CharacterID TEXT, Name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS Films (MovieID TEXT, Title TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS Directors (DirectorID TEXT, Name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS MoviesData (MovieID TEXT, CharacterID TEXT, DirectorID TEXT, Genre TEXT, Rating REAL, Runtime INTEGER, Date INTEGER, Month INTEGER, Year INTEGER)''')

c.execute('''CREATE TABLE IF NOT EXISTS InvalidIDs (MovieID TEXT)''')

limit = 100
try:
    last_index = open('last_index1.txt', 'r')
    index = int(last_index.read()) + 1
except FileNotFoundError as e:
    index = 1

counter = 0
while True:
    movie_id = str(index).zfill(7)
    if requests.get("https://www.imdb.com/title/tt%s/" % movie_id).status_code == 404:
        print("Invalid index: %d \nCounter: %d\n" % (index, counter))
        c.execute('''INSERT INTO InvalidIDs VALUES (?)''', [movie_id])
        index += 1
    else:
        data = movies.get_movie(movie_id).data
        accepted = False
        is_film = data['kind'] is 'movie'
        has_title = 'title' in data
        has_director = 'directors' in data
        in_usa = 'United States' in data['countries'] if 'countries' in data else False
        if is_film and has_title and has_director and in_usa:
            accepted = True

            if 'cast' in data:
                performers = [[data['cast'][x].getID(), data['cast'][x].__str__()] for x in range(len(data['cast']))]
                for performer in performers:
                    c.execute('''SELECT CharacterID FROM Performers WHERE CharacterID = ?''', [performer[0]])
                    if c.fetchone() is None:
                        c.execute('''INSERT INTO Performers VALUES (?,?)''', performer)

            movie = [movie_id, data['title']]
            c.execute('''INSERT INTO Films VALUES (?,?)''', movie)

            directors = [[data['directors'][x].getID(), data['directors'][x].__str__()] for x in range(len(data['directors']))]
            c.execute('''SELECT DirectorID FROM Directors''')
            for director in directors:
                c.execute('''SELECT DirectorID FROM Directors WHERE DirectorID = ?''', [director[0]])
                if c.fetchone() is None:
                    c.execute('''INSERT INTO Directors VALUES (?,?)''', director)

            month_abbr = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                          'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12, None: None}

            has_date = False
            if 'original air date' in data:
                has_date = True
                if data['original air date'][0] in "0123" and data['original air date'][2] is ' ':
                    date_temp = int(data['original air date'][:2])
                    month_temp = data['original air date'][3:6]
                elif data['original air date'][3] is ' ':
                    date_temp = None
                    month_temp = data['original air date'][:3]
                else:
                    date_temp = None
                    month_temp = None

            genre = data['year'] if 'year' in data else None
            rating = data['rating'] if 'rating' in data else None
            runtime = int(data['runtimes'][0]) if 'runtimes' in data else None
            date = date_temp if has_date else None
            month = month_abbr[month_temp] if has_date else None
            year = data['year'] if 'year' in data else None

            for x in range(len(data['cast'] if 'cast' in data else '1')):
                for y in range(len(data['directors'])):
                    c.execute('''INSERT INTO MoviesData VALUES (?,?,?,?,?,?,?,?,?)''', [movie_id,
                                                                                        data['cast'][x].getID() if 'cast' in data else None,
                                                                                        data['directors'][y].getID(),
                                                                                        genre, rating, runtime, date, month, year])

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
