#v0.2 bs4 - 20 Aug 21 - modified from googlnews_latest.py by YM
from bs4 import BeautifulSoup
import requests
import pandas as pd
import random
import time

user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
]

articles = []
status = True

# craft URL
query = 'semiconductor'     #change keyword here - for multiple keywords, use '+'. e.g 'microchips+production'
region = 'china'            #input location here.
start_date = '2021-01-01'   #search date from.
end_date = '2021-01-31'     #search date until.
start_url = f'https://www.google.com/search?q={region}+{query}+after:{start_date}+before:{end_date}&source=lnms&tbm=nws&sa=X&ved=2ahUKEwiE772fyL3yAhUHOSsKHbDACH8Q_AUoAnoECAEQBA&biw=1350&bih=1052'

# define header
user_agent = ""
for i in range(1):
    user_agent = random.choice(user_agent_list)
headers = {'User-Agent': user_agent}

# getArticles function
def getArticles():
    global start_url
    r = requests.get(start_url, headers=headers)
    print(r)
    soup = BeautifulSoup(r.text, 'lxml')
    posts = soup.find_all('div', {'class': 'dbsr'})

    for post in posts:
        article = {
            'query' : query,
            'region' : region,
            'title' :  post.find('div', {'class' : 'JheGif nDgy9d'}).text,
            'excerpt' : post.find('div', {'class' : 'Y3v8qd'}).text,
            'date' : post.find('span', {'class' : 'WG9SHc'}).span.text,
            'source' : post.find('div', {'class' : 'XTjFC WF4CUc'}).text,
            'link': post.find('a').get('href')
        }
        articles.append(article)

# Change the URL to next page URL
def nextURL():
    global start_url, status
    try:
        r = requests.get(start_url, headers=headers)
        print(r)
        soup = BeautifulSoup(r.text, 'lxml')
        next = soup.find('a', {'id':'pnnext'}).get('href')
        start_url = "https://google.com" + next
        status = True
        print(status)
    except:
        status = False
        print(status)



# Looping through all Pagination
while status == True:
    getArticles()
    nextURL()
    
# Store to dataframe then to CSV
df = pd.DataFrame(articles)
df.to_csv(str(query)+str(start_date)+'to'+str(end_date)+'.csv')
print(len(articles))



