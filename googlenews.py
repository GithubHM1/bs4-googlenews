from bs4 import BeautifulSoup
import requests
import pandas as pd

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
headers = {'User-Agent': user_agent}
articles = []

def getArticles(query,page):
    url = f'https://www.google.com/search?q={query}&rlz=1C1ONGR_enSG933SG933&tbm=nws&sxsrf=ALeKk02tCHQynr04rQShXIFAfuYaxN1CwQ:1628523605027&ei=VUwRYYBjkt31A-GBidgJ&start={page}&sa=N&ved=2ahUKEwjA4fCXo6TyAhWSbn0KHeFAApsQ8tMDegQIBxA2&biw=1920&bih=969&dpr=1'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    
    posts = soup.find_all('div', {'class': 'yr3B8d KWQBje'})

    for post in posts:
        article = {
            'query' : query,
            'title' :  post.find('div', {'class' : 'JheGif nDgy9d'}).text,
            'source' : post.find('div', {'class' : 'XTjFC WF4CUc'}).text,
            'excerpt' : post.find('div', {'class' : 'Y3v8qd'}).text,
            'date' : post.find('span', {'class' : 'WG9SHc'}).span.text
        }
        articles.append(article)


i = 0
while i < 321:
    getArticles('semiconductor', i )
    getArticles('microchip', i)
    i += 10


df = pd.DataFrame(articles)
df.to_csv('combined.csv')
print(len(articles))



