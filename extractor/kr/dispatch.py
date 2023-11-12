import requests
import datetime

from client.user_agent import InitUserAgent
from bs4 import BeautifulSoup
from common.data_structure import Site, ScrapperPayload

SITE_INFO = Site(hostname="dispatch.co.kr", name="Dispatch", location="KR")

def get_data(hd):
    r = requests.get(hd, headers={'User-Agent': InitUserAgent().get_user_agent()})
    soup = BeautifulSoup(r.text, 'html.parser')
    img_list = []
    post_date = soup.find('div', class_='post-date').text.strip()
    post_title = soup.find('div', class_='page-post-title').string.strip()
    post_date_short = post_date.replace('.', '')[2:8]

    for i in soup.findAll('img', class_='post-image'):
        if i.get('data-src') != None:
            if i.get('data-src').startswith('<' or '>'):
                continue
            temp = i.get('data-src')
            img_list.append(temp)
        else:
            if i.get('src').startswith('<' or '>'):
                continue
            temp = i.get('src')
            img_list.append(temp)

    post_date = post_date[:19].replace('.', '')
    if '오전' in post_date:
        post_date = datetime.datetime.strptime(post_date.replace('오전', 'AM'), '%Y%m%d %p %I:%M')
    elif '오후' in post_date:
        post_date = datetime.datetime.strptime(post_date.replace('오후', 'PM'), '%Y%m%d %p %I:%M')

    print("Title: %s" % post_title)
    print("Date: %s" % post_date)
    print("Found %s image(s)" % len(img_list))

    payload = ScrapperPayload(
        title=post_title,
        shortDate=post_date_short,
        mediaDate=post_date,
        site=SITE_INFO.name,
        series=None,
        writer=None,
        location=SITE_INFO.location,
        media=img_list,
    )

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory_alternate(payload)