import requests
from bs4 import BeautifulSoup
import re

####################
#                  #
# DEFINE VARIABLES #
#                  #
####################

main_page_url_a = "https://www.imdb.com/search/title/?title_type=feature&release_date=2010-01-01,2020-12-31&user_rating=1.0,10.0&countries=US&languages=en&sort=release_date,asc&start="
main_page_url_b = "&ref_=adv_nxt"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

####################
#                  #
# DEFINE FUNCTIONS #
#                  #
####################

def filter_and_remove_duplicate_urls(url_list):
    clean_urls = set()

    filtered_urls = [url for url in url_list if url.startswith('/title')]

    for url in filtered_urls:
        if url.startswith('/title'):
            parts = url.split('/')
            if len(parts) >= 2:
                clean_urls.add('/title/' + parts[2])

    return list(clean_urls)

def extract_box_office_info(soup):
    box_office_elements = ["budget", "grossdomestic", "openingweekenddomestic", "cumulativeworldwidegross"]

    box_office_element_values = list()

    for i in box_office_elements:

        box_office_element = soup.find('li', attrs={'data-testid': f'title-boxoffice-{i}'})

        if box_office_element:
            ul_element = box_office_element.find('ul')
            if ul_element:
                li_element = ul_element.find('li')
                if li_element:
                    span_element = li_element.find('span')
                    if span_element:
                        box_office_element_values.append(span_element.text.strip())
    
    return box_office_element_values

def extract_release_date(soup):
    release_date_element = soup.find('li', attrs={'data-testid': 'title-details-releasedate'})
    
    if release_date_element:
        ul_element = release_date_element.find('ul')
        if ul_element:
            li_element = ul_element.find('li')
            if li_element:
                a_element = li_element.find('a')
                if a_element:
                    return a_element.text.strip()
    
    return None

def extract_country_of_origin(soup):
    origin_element = soup.find('li', attrs={'data-testid': 'title-details-origin'})

    if origin_element:
        ul_element = origin_element.find('ul')
        if ul_element:
            li_element = ul_element.find('li')
            if li_element:
                a_element = li_element.find('a')
                if a_element:
                    return a_element.text.strip()

    return None

def extract_movie_runtime(soup):
    runtime_element = soup.find('li', attrs={'data-testid': 'title-techspec_runtime'})

    if runtime_element:
        div_element = runtime_element.find('div')
        if div_element:
            # Extract all text within the div element and concatenate it
            runtime_text = ' '.join(div_element.stripped_strings)
            return runtime_text

    return None

def get_the_subpage(url):
    subpage = requests.get("https://imdb.com" + url, headers=headers)
    subpage_soup = BeautifulSoup(subpage.text)

    info = extract_box_office_info(subpage_soup)
    info.append(extract_release_date(subpage_soup))
    info.append(extract_country_of_origin(subpage_soup))
    info.append(extract_movie_runtime(subpage_soup))

    if len(info) > 0:
        return info
    else:
        return None

###################
#                 #
# PROGRAM RUNNING #
#                 #
###################

file = open("revenue.txt", "w", encoding="utf-8")
file.write("URL; grossdomestic; openingweekendsdomestic; cumulativeworldwidegross; releasedate; countryoforigin; runtime;\n")

for i in range(460):
    print("current page: " + str(i+1))

    content = requests.get(main_page_url_a + str(i*50+1) + main_page_url_b)
    print(content)

    soup = BeautifulSoup(content.text)
    links = list()

    for i in soup.find_all("a"):
        url = i.get('href')
        links.append(url)

    filtered_links = filter_and_remove_duplicate_urls(links)

    for i, n in enumerate(filtered_links):
        file.write(str(n) + "; ")

        subpage_contents = get_the_subpage(filtered_links[i])

        for j, r in enumerate(subpage_contents):
            file.write(str(r) + "; ")
        
        file.write("\n")

        print("current subpage: " + str(i+1) + "/50")

file.close