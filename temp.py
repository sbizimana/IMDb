import requests

for x in range(10):
    request = requests.get("https://www.imdb.com/title/tt%s/" % str(7740355).zfill(7))
    print(request.status_code)
    if x == 9:
        x = 7740355