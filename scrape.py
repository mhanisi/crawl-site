import requests
from bs4 import BeautifulSoup
from newspaper import Article
from tqdm import tqdm
import pandas

page_links_count = 2

def crawl ():
    done = False
    data = []
    page = 9

    last_url = ''
    while True:
        url = f"https://khabarfarsi.com/latest-news/2470?page={page}"
        page = page + 1
        html = requests.get(url).text
        soup = BeautifulSoup(html, features="lxml")
        lists = soup.find_all("div", {"class": "top_item_wrapper"})

        if done: break

        for index, list in enumerate(lists):
            if index >= page_links_count: break;
            links = list.find_all("h2")
            print(links)
            for link in tqdm(links):
                path = link.find('a')['href']
                url = "https://khabarfarsi.com" + path

                if index == 0:
                    if (last_url == url):
                        done = True
                        break;
                    last_url = url

                try:
                    article = Article(url)
                    article.download()
                    article.parse()
                    data.append({"url": url, "text": article.text, "title": article.title})
                except:
                    print(f"Failed to load {url}")
    
    df = pandas.DataFrame(data)
    df.to_csv(f"kabar_farsi.csv")


crawl()