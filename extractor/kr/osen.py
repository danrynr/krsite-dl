import requests
import datetime

from client.user_agent import InitUserAgent
from bs4 import BeautifulSoup

def from_osen(hd, loc, folder_name):
    r = requests.get(hd, headers={'User-Agent': InitUserAgent().get_user_agent()})
    soup = BeautifulSoup(r.text, 'html.parser')
    wrap = soup.find('div', class_='detailTitle')

    post_title = wrap.find('h1').text
    post_date = soup.find('div', class_='detailTitle__post-infos').text.strip()

    img_list = []

    for item in soup.findAll('img', class_='view_photo'):
        img_list.append('https:' + item['src'].split(':')[1])

    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%d %H:%M')
    post_date_short = post_date.strftime('%Y%m%d')[2:]

    print("Post title: %s" % post_title)
    print("Post date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))
    
    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory_combine(img_list, post_title, post_date, post_date_short, loc, folder_name)