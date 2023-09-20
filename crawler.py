import requests
from bs4 import BeautifulSoup
import queue
import re
import time
import random


def get_html(url):
    try:
        return requests.get(url).content
    except Exception as e:
        print(e)
        return ''


def crawl_page(soup, url, visited_urls, urls):
    link_elements = soup.select("a[href]")
    for link_element in link_elements:
        url = link_element['href']
        
        if re.match(r"https://(?:.*\.)?scrapeme\.live", url):
            if url not in visited_urls and url not in [item[1] for item in urls.queue]:
                priority_score = 1
                if re.match(r"^https://scrapeme\.live/shop/page/\d+/?$", url):
                    priority_score = 0.5
                urls.put((priority_score, url))


def scrape_page(soup, url, products):
    product = {}
    product["url"] = url
    product["title"] = soup.select_one("h1").text()
    products.push(product)


urls = queue.PriorityQueue()
urls.put((0.5, "https://scrapeme.live/shop/"))
visited_urls = []

while not urls.empty():
    _, current_url = urls.get()
    soup = BeautifulSoup(get_html(current_url), "html.parser")
    
    visited_urls.append(current_url)
    crawl_page(soup, current_url, visited_urls, urls)
    
# if it is a product page:
    # scrape_page(soup, url, products)