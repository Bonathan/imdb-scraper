import requests
from bs4 import BeautifulSoup
import re

revenue = list()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

def filter_and_remove_duplicates(url_list):
    clean_urls = set()

    # this first removes all the links that don't start with "/title/..."
    filtered_urls = [url for url in url_list if url.startswith('/title')]
    
    # this cleans up the list of "/title/..." urls, by ignoring the vote/plotsummaries/etc
    for url in filtered_urls:
        if url.startswith('/title'):
            # Split the URL by '/' and take the first part after '/title'
            parts = url.split('/')
            if len(parts) >= 2:
                clean_urls.add('/title/' + parts[2])

    return list(clean_urls)

        # extracts the box-office infos
def extract_box_office_info(soup, info_type):
    box_office_element = soup.find('li', attrs={'data-testid': f'title-boxoffice-{info_type}'})
    
    if box_office_element:
        ul_element = box_office_element.find('ul')
        if ul_element:
            li_element = ul_element.find('li')
            if li_element:
                span_element = li_element.find('span')
                if span_element:
                    return span_element.text.strip()
    
    return None


def get_the_subpage(url):
    
    subpage = requests.get("https://imdb.com" + url, headers=headers)
    subpage_soup = BeautifulSoup(subpage.text, features="lxml")

    # print(subpage.text)
    # print("https://imdb.com" + url)

    movie_money = ["budget", "grossdomestic", "openingweekenddomestic", "cumulativeworldwidegross"]

    money = list()

    # data-testid="title-boxoffice-budget"
    # data-testid="title-boxoffice-grossdomestic"
    # data-testid="title-boxoffice-openingweekenddomestic"
    # data-testid="title-boxoffice-cumulativeworldwidegross"

    for i in movie_money:
        print(extract_box_office_info(subpage_soup, i))
        money.append(extract_box_office_info(subpage_soup, i))
    
    if len(money) > 0:

        return money
        
    else:
        return None

# define the url for the page to be indexed
# main_page_url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2010-01-01,2020-12-31&user_rating=1.0,10.0&countries=US&languages=en&sort=release_date,asc&start=1&ref_=adv_nxt"
main_page_url_a = "https://www.imdb.com/search/title/?title_type=feature&release_date=2010-01-01,2020-12-31&user_rating=1.0,10.0&countries=US&languages=en&sort=release_date,asc&start="
main_page_url_b = "&ref_=adv_nxt"

for i in range(460):
    print(i)

    # GET request
    content = requests.get(main_page_url_a + str(i*50+1) + main_page_url_b)

    # write it to a file -> for trial purposes demo.html
    # main_page = open("demo.html", "w")
    # main_page.write(content.text)
    # main_page.close()

    # initialize soup
    soup = BeautifulSoup(content.text, features="lxml")
    links = list()

    # isolate all links on the webpage
    for link in soup.find_all("a"):
        url = link.get('href')
        links.append(url)

    # filter the links using the function defined above
    filtered_links = filter_and_remove_duplicates(links)

    links_file = open("links.txt", "a")
    links_file.write(str(filtered_links))
    links_file.close

    for i, n in enumerate(filtered_links):

            revenue_file = open("revenue.txt", "a")
            revenue_file.write(str(n) + "; ")
            revenue_file.close  

            subpage_contents = get_the_subpage(filtered_links[i])

            for j, r in enumerate(subpage_contents):
                print("subpage: " + str(i) + str(r))
                revenue_file = open("revenue.txt", "a")
                revenue_file.write(str(r) + "; ")
                revenue_file.close  

            revenue_file = open("revenue.txt", "a")
            revenue_file.write("\n")
            revenue_file.close

    # print the amount of links, to make sure everything went right
    # print(len(filtered_links))

    for j in range(50):
        # print("i: " + str(i))
        get_the_subpage(filtered_links[i])





print(revenue)

get_the_subpage("/title/tt1053424/")