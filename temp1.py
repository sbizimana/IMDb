import imdb

movies = imdb.IMDb()

data = movies.get_movie('0002927').data
print(type(data['genres']))

performers = [[data['cast'][x].getID(), data['cast'][x].__str__()] for x in range(len(data['cast']))]
print(performers)