import imdb


movies = imdb.IMDb()

x = movies.get_movie('0002927').data
print(x)

print('color info' in x)
print('countries' in x)