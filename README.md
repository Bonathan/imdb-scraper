# imdb-scraper
little, more or less lightweight, python imdb scraper for box office data

## dependencies
- requests (for HTTP requests)
- BeautifulSoup from bs4 (to filter through the HTML content)
- re (regular expression to filter the list with URLs)

## usage
with the dependencies installed, run `scraper.py`. it will print in the output what page it's on (pages one to 460). it will write the URL and the box office information in a text file (`revenue.txt`), separated by semicolons.
```
/title/tt1053424; $32,000,000 (estimated); $13,794,835; $6,126,170; $18,409,891;
/title/tt1535568; $500,000 (estimated); $20,615; $2,966; $20,615;
/title/tt1277144; $205,000 (estimated); None; None; None;
```

if there is no information in the corresponding field, it will be filled with `None`.
