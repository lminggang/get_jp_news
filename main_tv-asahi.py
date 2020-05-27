import os
import time
import urllib.parse
import requests
from lxml import etree

base_host = 'https://post.tv-asahi.co.jp'
base_url = os.path.join(base_host)

record_url_list = set()

def check_folder(path=''):
    if path[-1] != '/':
        check_path = '/'.join(path.split('/')[:-1])
    else:
        check_path = '/'.join(path.split('/')[:-2])
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
    if not path:
        return None

    path_id = path.split('-')[-1]

    if not path_id.isdigit():
        return None

    check_folder(path=path)

    with open(path, 'w+b') as _file:
        _file.write(content)
    return True

def href_handle(href):
    if not href:
        return False

    if href[0] == '/':
        href = '{}{}'.format(base_url, href)

    if href[:len(base_url)] != base_url:
        return False

    return href

def request_href(url):
    if url in record_url_list:
        return None

    print(url)
    record_url_list.add(url)

    try:
        res = requests.get(url, timeout=2)
    except Exception as e:
        return None
    content = res.content
    save_res = save_content(url=url, content=content)
    time.sleep(0.1)
    dom = etree.HTML(content)
    href_list = dom.xpath('//a/@href')
    href_list = [href for href in href_list if '#' not in href]
    new_href_list = list()
    for href in href_list:
        href = href_handle(href)
        if href:

            if href[-1] == '/':
                href = href[:-1]
            new_href_list.append(href.strip())
    return new_href_list
        # request_href(href)

def main():
    base_host = 'https://post.tv-asahi.co.jp'
    base_url = os.path.join(base_host)
    href_list = request_href(base_url)
    new_href_list = list()
    while True:
        for href in href_list:
            res = request_href(href)
            if res: 
                new_href_list += res

        href_list = new_href_list
        new_href_list = list()


if __name__ == '__main__':
    while True:
        try:
            print('start request... [{}]'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
            main()
            time.sleep(5)
        except Exception as e:
            print(e)
            time.sleep(30)
        
