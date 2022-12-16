import string
import requests
from bs4 import BeautifulSoup
import os

url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page='
page_number = int(input())
article_input = str(input())


# Loop through the specified number of pages
for i in range(1, page_number + 1):
    page_url = url + str(i)
    dir_name = 'Page_' + str(i)
    os.mkdir(dir_name)

    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all("article")

    # Search the page for articles
    for article in articles:
        type_span = article.find("span", {"data-test": "article.type"})
        article_type = type_span.text.strip()

        # Search the page for articles of the specified type
        if article_type == article_input:
            link_a = article.find("a", {"data-track-action": "view article"})
            link = "http://www.nature.com" + link_a['href']

            article_response = requests.get(link)
            article_soup = BeautifulSoup(article_response.text, 'html.parser')

            article_title = article_soup.find("h1").text
            filename = article_title.replace(" ", "_").strip(string.punctuation) + ".txt"
            article_body = article_soup.find("div", {"class": "c-article-body main-content"}).text.strip()

            with open(os.path.join(dir_name, filename), "wb") as f:
                f.write(article_body.encode("UTF-8"))
