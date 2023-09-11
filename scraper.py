from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import requests
import json
import gspread

gc = gspread.service_account(filename='credentials.json')
sh = gc.open('P2').sheet1
sh.batch_clear(['A:E'])
sh.append_row(['Titular', 'Categoría', 'Autor', 'Tiempo de Lectura', 'Fecha de publicación'])



class sheetEntry (): 
    def __init__(self, title, category, author, readingTime, date):
        self.title = title
        self.category = category
        self.author = author
        self.readingTime = readingTime
        self.date = date
        
category = "pymes".lower()
baseUrl = "https://xepelin.com/blog/" + category
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1480')
driver = webdriver.Chrome(options)
driver.get(baseUrl)
encode = "utf-8"
html = driver.page_source.encode(encode)
timeToSleep = 2

time.sleep(timeToSleep)
try:
    while driver.find_element(By.XPATH, '//button[text()="Cargar más"]'):
        driver.find_element(By.XPATH, '//button[text()="Cargar más"]').click()
        print("Getting next part")
        time.sleep(timeToSleep)
except:
    pass

html = driver.page_source.encode(encode)

soup = BeautifulSoup(html, 'lxml')
articles = soup.find_all('div', attrs={"class": "BlogArticle_box__OYCvH"})
entries = []

for post in articles:
    url = post.find('a', href=True)['href']
    #print(f"El url {url}")
    blogHtml = requests.get(url)
    blogSoup = BeautifulSoup(blogHtml.text, 'html.parser')
    title = blogSoup.find('h1').get_text()
    # Header issue
    readingTime = blogSoup.find('div', attrs={"class": "Text_body__ldD0k"}).get_text()
    #date = blogSoup.find('p', attrs={"class": "NewsArticle_date__aLEvo"})
    date = json.loads(blogSoup.find('script', attrs={"id": "__NEXT_DATA__"}).get_text())['props']['pageProps']['article']['_createdAt']
    author = blogSoup.find('div', attrs={"class": "Text_bodySmall__wdsbZ"}).get_text()
    print(f"{title} | {author} | {category} | {date} | {readingTime}")
    entries.append(sheetEntry(title, category, author, readingTime, date))

for article in entries:
    sh.append_row([article.title, article.category, article.author, article.readingTime, article.date.split('T')[0]])


