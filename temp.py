import requests

x = 1
while True:
    status_code = requests.get("https://www.imdb.com/title/tt%s/" % str(x).zfill(7)).status_code
    print(x)
    if status_code == 404:
        break
    x += 1
