import os
import time
import urllib.parse
import requests
from lxml import etree

base_host = 'https://www.msn.com'
base_area = 'ja-jp'
base_url = os.path.join(base_host, base_area)
keyword_base = 'ja-jp'
keyword_other = 'news'
keyword_replace = '//www.msn.com'

record_url_list = list()

def check_folder(path=''):
    check_path = '/'.join(path.split('/')[:-1])
    if not os.path.exists(check_path):
        os.makedirs(check_path)


def url_to_path(url=''):
    path = ''
    if 'https://' in url:
        path = url[8:]
    elif 'http://' in url:
        path = url[7:]

    return urllib.parse.unquote(path)

def save_content(url, content):

    path = url_to_path(url=url)
    if not path or 'ar-' not in path:
        return None

    check_folder(path=path)

    with open(path, 'w+b') as _file:
        _file.write(content)
    return True

def request_href(url):
    if url in record_url_list:
        return None

    print(url)
    record_url_list.append(url)

    if 'commailto:?subject=' in url:
        return None
    try:
        res = requests.get(url, timeout=2)
    except Exception as e:
        return None
    content = res.content
    save_res = save_content(url=url, content=content)
    time.sleep(0.1)

    dom = etree.HTML(content)
    href_list = dom.xpath('//a/@href')
    href_list = [href for href in href_list if 'ja-jp' in href]
    new_href_list = list()
    for href in href_list:
        if keyword_base in href or keyword_other in href:
            if r'//' in href:
                if 'www.msn.com'  not in href:
                    continue

            if keyword_replace in href:
                new_href = href.replace(keyword_replace, base_host)
            else:
                new_href = '{}{}'.format(base_host, href)

            request_href(new_href)



if __name__ == '__main__':
    while True:
        print('start request...')
        href_list = request_href(base_url)
