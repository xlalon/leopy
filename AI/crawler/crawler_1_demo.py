# -*- coding: utf -*-

import urllib.parse
import urllib.request
from fake_useragent import UserAgent


def get_url(url, method='GET', query=None, body=None, headers={}, username=None, passwd=None, proxy=None):
    if query:
        url = '{}?{}'.format(url, urllib.parse.urlencode(query))
    if body:
        body = urllib.parse.urlencode(body)
    # if username and passwd:
    #     auth_info = urllib.request.HTTPBasicAuthHandler()
    #     auth_info.add_password(user=username, passwd=passwd)
    #     proxy = urllib.request.ProxyHandler(proxies=proxy)
    #     opener = urllib.request.build_opener(auth_info, proxy)
    #     urllib.request.install_opener(opener)
    #     return urllib.request.urlopen(url).read()
    request = urllib.request.Request(url, method=method, data=body, headers=headers)
    response = urllib.request.urlopen(request)
    return response.read()


def fake_user_agent():
    ua = UserAgent(verify_ssl=False)
    return ua.chrome


def header_with_fake_ua():
    fake_ua = fake_user_agent()
    return {'User-Agent': fake_ua}


if __name__ == '__main__':
    print(header_with_fake_ua())
    # print(get_url('https://www.qidian.com/'))
