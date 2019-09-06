import requests

import urllib.parse

from requests.exceptions import RequestException

from urllib.parse import urljoin

from lxml import etree
import re
import json
import pandas as pd
import numpy as np

# 百度搜索接口


def format_url(url, params: dict = None) -> str:
    query_str = urllib.parse.urlencode(params)
    return f'{ url }?{ query_str }'


def get_url(keyword):
    params = {
        'wd': str(keyword)
    }
    url = "https://www.baidu.com/s"
    url = format_url(url, params)
    # print(url)

    return url


def get_page(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}
        response = requests.get(url=url, headers=headers)
        # 更改编码方式，否则会出现乱码的情况
        response.encoding = "utf-8"
        print(response.status_code)
        # print(response.text)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_page(url, page):

    for i in range(1, int(page) + 1):
        print("正在爬取第{}页....".format(i))
        title = ""
        sub_url = ""
        abstract = ""
        flag = 11
        if i == 1:
            flag = 10
        html = get_page(url)
        content = etree.HTML(html)
        for j in range(1, flag):
            data = {}
            res_title = content.xpath(
                '//*[@id="%d"]/h3/a' %
                ((i - 1) * 10 + j))
            if res_title:
                title = res_title[0].xpath('string(.)')

            sub_url = content.xpath(
                '//*[@id="%d"]/h3/a/@href' %
                ((i - 1) * 10 + j))
            if sub_url:
                sub_url = sub_url[0]

            res_abstract = content.xpath(
                '//*[@id="%d"]/div[@class="c-abstract"]' %
                ((i - 1) * 10 + j))
            if res_abstract:
                abstract = res_abstract[0].xpath('string(.)')
                # i='违规'
                # if i not in abstract:
                #     abstract=[]

            else:
                res_abstract = content.xpath(
                    '//*[@id="%d"]/div/div[2]/div[@class="c-abstract"]' %
                    ((i - 1) * 10 + j))
                if res_abstract:
                    abstract = res_abstract[0].xpath('string(.)')
                    # i = '违规'
                    # if i not in abstract:
                    #     abstract = []
                    # res_abstract = content.xpath('//*[@id="%d"]/div/div[2]/p[1]'%((i-1)*10+j))
            # if not abstract:
            #     abstract = content.xpath('//*[@id="%d"]/div/div[2]/p[1]'%((i-1)*10+j))[0].xpath('string(.)')
            data['title'] = title
            data['sub_url'] = sub_url
            data['abstract'] = abstract

            rel_url = content.xpath('//*[@id="page"]/a[{}]/@href'.format(flag))
            # if rel_url:
            #     url = urljoin(url, rel_url[0])
            # else:
            #     print("无更多页面！～")
            #     return
            yield data


def main():
    keyword = input("输入关键字:")
    page = input("输入查找页数:")
    url = get_url(keyword)

    results = parse_page(url, page)
    # 写入文件
    # file = open("data.json", 'w+', encoding='utf-8')
    result_store = []
    for result in results:
        i = '违纪'
        if i in result['abstract']:

            print(result)
            # file.write(json.dumps(result, indent=2, ensure_ascii=False))
            data = pd.DataFrame({'标题': (result['title']), '链接': (
                result['sub_url']), '内容': (result['abstract'])}, index=[0])  # 设置索引
            result_store.append(data)
    final_result = pd.concat(result_store, ignore_index=True)
    final_result = final_result.drop_duplicates()
    print(final_result)
    final_result.to_csv(
        'C:\\Users\\Administrator\\Desktop\\文件\\baidu.csv',
        index=False)

def content():
    Result=[]
    keyword='陕西能源赵石畔王栋'
    page=10
    path='C:\\Users\\Administrator\\Desktop\\文件\\data\\'
    for i in word_list():
        search_word=''
        search_word=keyword+i
        url=get_url(search_word)
        results = parse_page(url, page)
        result_store = []
        for result in results:

            if i in result['abstract']:
                print(result)
                # file.write(json.dumps(result, indent=2, ensure_ascii=False))
                data = pd.DataFrame({'标题': (result['title']), '链接': (
                    result['sub_url']), '内容': (result['abstract'])}, index=[0])  # 设置索引
                result_store.append(data)
        if result_store == []:
            print('无数据')
        else:
            final_result = pd.concat(result_store, ignore_index=True)
            final_result = final_result.drop_duplicates()
            Result.append(final_result)
    Result=pd.concat(Result,ignore_index=True)
    Result=Result.drop_duplicates()
    print(Result)
    Result.to_csv(path+keyword+'.csv',index=False)
            # print(final_result)
            # final_result.to_csv(path +search_word+ '.csv', index=False)




def word_list():
    file = ('C:\\Users\\Administrator\\Desktop\\文件\\word.txt')
    word_store = []
    with open(file, 'r') as f:
        for i in f.readlines():
            word_store.append(i.strip())
    return word_store


if __name__ == '__main__':
    c = word_list()
    content()




    # main()
