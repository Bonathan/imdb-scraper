# imdb-scraper
little, more or less lightweight, python imdb scraper for box office data

## dependencies
- requests (for HTTP requests)
- BeautifulSoup from bs4 (to filter through the HTML content)
- re (regular expression to filter the list with URLs)

## usage
with the dependencies installed, run `scraper.py`. it will print in the output what page it's on (pages one to 460), and what subpage (pages one to 50, per each of the 460 pages). it will write the URL and the box office information in a text file (`revenue.txt`), separated by semicolons.
```
URL; grossdomestic; openingweekendsdomestic; cumulativeworldwidegross; releasedate; countryoforigin; runtime;
```

if there is no information in the corresponding field, it will be filled with `None`. the creation/maintenance of the `revenue.txt` file will be handled automatically, there is no need to delete it, as the program wipes it, when starting. furthermore, the `revenue.txt` file will be ignored by git.

## todo
I could add the following things:
- average IMDb user rating
- amount of ratings
- awards
- amount of user reviews
- amount of critic reviews
- metascore
- Cast (?)
- Director (?)
- Production Company (?)