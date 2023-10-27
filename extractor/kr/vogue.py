import requests
import datetime

from client.user_agent import InitUserAgent
from common.data_structure import Site, ScrapperPayload
from pytz import timezone
from bs4 import BeautifulSoup

SITE_INFO = Site(hostname="vogue.co.kr", name="Vogue Korea", location="KR")
                 
def get_data(hd):
    r = requests.get(hd, headers={'User-Agent': InitUserAgent().get_user_agent()})
    soup = BeautifulSoup(r.text, 'html.parser')

    post_title = soup.find('meta', property='og:title')['content'].strip()
    post_date = soup.find('meta', property='article:published_time')['content'].strip()
    post_date_short = post_date.replace('-', '')[2:8]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%dT%H:%M:%S%z')
    tz = timezone('Asia/Seoul')
    post_date = post_date.astimezone(tz).replace(tzinfo=None)

    content = soup.find('div', class_='contt')

    # print(content)

    img_list = []

    for item in content.findAll('img'):
        if item.get('data-src') is not None:
            i = item.get('data-src')
            img_list.append(i.split('-')[0] + '.' + i.split('.')[-1])

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

    DirectoryHandler().handle_directory(payload)