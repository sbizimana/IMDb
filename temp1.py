import imdb

movies = imdb.IMDb()

data = movies.get_movie('0000501').data
print(data['original air date'])

performers = [[data['cast'][x].getID(), data['cast'][x].__str__()] for x in range(len(data['cast']))]
print(performers)