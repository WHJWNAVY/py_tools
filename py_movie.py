import sys
import re
import time
import os
import random
import requests
import json
import lxml.html
from lxml import etree
from urllib import parse

# user_agent列表，每次执行requests请求都随机使用该列表中的user_agent，避免服务器反爬
user_agent_list = [
    # Windows / Firefox 58
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0",
    # Linux / Firefox 58
    "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
    # Mac OS X / Safari 11.0.2
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_2) AppleWebKit/603.1.13 (KHTML, like Gecko) Version/11.0.2 Safari/603.1.13",
    # Windows / IE 11
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    # Windows / Edge 16
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/16.16299.15.0",
    # Windows / Chrome 63
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    # Android Phone / Chrome 63
    "Mozilla/5.0 (Linux; Android 7.0; SM-G935P Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36",
    # Android Tablet / Chrome 63
    "Mozilla/5.0 (Linux; Android 4.4.4; Lenovo TAB 2 A10-70L Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Safari/537.36",
    # iPhone / Safari 11.1.1
    # "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/11.1.1 Mobile/14E304 Safari/602.1",
    # iPad / Safari 11.1.1
    "Mozilla/5.0 (iPad; CPU OS 11_1_1 like Mac OS X) AppleWebKit/603.3.3 (KHTML, like Gecko) Version/11.1.1 Mobile/14G5037b Safari/602.1"]

# requests请求头
requests_header = {
    "Accept": "text/html,application/xhtml+xml,aplication/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.5",
    "Cache-Control": "max-age=0",
    "Connection": "close",  # "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    # "Host": "www.ygdy8.com",
    # "Host": "s.ygdy8.com",
    "User-Agent": "",
    # "Cookie": "XLA_CI=cf1074d18fsad508118bf49070f839edd",
    # "Cookie": "PHPSESSID=c78d8d9cec1c9cc5d4ad1b7b853c8865",
    "If-Modified-Since": "Mon, 15 Oct 2018 05:00:56 GMT",
    "If-None-Match": "0b43ce4464d41:6b2",
}

host_cookie = [["s.ygdy8.com", "PHPSESSID=c78d8d9cec1c9cc5d4ad1b7b853c8865"],
               ["www.ygdy8.com", "XLA_CI=cf1074d18fsad508118bf49070f839edd"],
               ["movie.douban.com", "bid=Qcxxo1zGY-0; ll=\"118318\"; "
                "_pk_id.100001.4cf6=d0643332f19ceb25.1540174085.1.1540174085.1540174085.; "
                "_pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.1196349838.1540174085.1540174085.1540174085.1; "
                "__utmb=30149280.0.10.1540174085; __utmc=30149280; "
                "__utmz=30149280.1540174085.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); "
                "__utma=223695111.1123720872.1540174085.1540174085.1540174085.1; __utmb=223695111.0.10.1540174085; "
                "__utmc=223695111; __utmz=223695111.1540174085.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); "
                "__yadk_uid=niaGvj3qwbFWQEzvAM79JiSkBFNd1qjD; "
                "_vwo_uuid_v2=D38F372B15258169D50B0D6D5264A3B1E|653f83f60dc7f293f84af6645346eee3"]]


def download_page_html(url, sel=0):
    phtml = None
    page = None
    try:

        # if sel == 0:
        #     requests_header["Host"] = "s.ygdy8.com"
        #     requests_header["Cookie"] = "PHPSESSID=c78d8d9cec1c9cc5d4ad1b7b853c8865"
        # else:
        #     requests_header["Host"] = "www.ygdy8.com"
        #     requests_header["Cookie"] = "XLA_CI=cf1074d18fsad508118bf49070f839edd"

        # if sel > len(host_cookie):
        #     print("参数错误!")
        #     return None

        requests_header["Host"] = host_cookie[sel][0]
        requests_header["Cookie"] = host_cookie[sel][1]

        # 选择一个随机的User-Agent
        requests_header["User-Agent"] = random.choice(user_agent_list)
        # print(requests_header["User-Agent"])
        # print(requests_header)
        page = requests.get(url=url, headers=requests_header,
                            timeout=15)  # 请求指定的页面
        # print(page.encoding)
        if page.encoding == "ISO-8859-1":
            page.encoding = "gb2312"  # 转换页面的编码为gb2312(避免中文乱码)
        phtml = page.text  # 提取请求结果中包含的html文本
        # print("requests success")
        # page.close()  # 关闭requests请求
    except requests.exceptions.RequestException as e:
        print("requests error:", e)
        phtml = None
        # if page != None:
        #     page.close()
    finally:
        if page != None:
            page.close()
        return phtml


def movie_tiantang(mvsearch_name):
    MVSEARCH_URL = "http://s.ygdy8.com/plus/so.php"
    MVSEARCH_PAR = {"kwtype": "0", "searchtype": "title",
                    "pagesize": "100", "keyword": ""}
    MOVIE_URL = "http://www.ygdy8.com"

    # mvsearch_name = "星球大战"
    # mvsearch_name = input("请输入电影名称(输入\"exit\"退出):")

    if mvsearch_name == None:
        print("输入有误!")
        return -1
    
    print("正在从电影天堂搜索", mvsearch_name)

    # print("你输入的电影名称为:", mvsearch_name)

    # 搜索电影
    MVSEARCH_PAR["keyword"] = mvsearch_name
    mvsearch_par = parse.urlencode(MVSEARCH_PAR, encoding="gb2312")
    # print(mvsearch_par)
    mvsearch_url = "{0}?{1}".format(MVSEARCH_URL, mvsearch_par)
    # print(mvsearch_url)
    mvsearch_html = download_page_html(mvsearch_url, 0)
    if mvsearch_html == None:
        print("下载出错,可能IP被服务器封禁,可稍后再试!")
        return -1

    # print(mvsearch_html)

    # 获取搜索结果列表
    etree_html = lxml.html.fromstring(mvsearch_html)
    # print(type(etree_html))
    # print(etree.tostring(etree_html, encoding="utf-8").decode("utf-8"))
    mvsearch_xpath = '//div[@class="co_content8"]/ul/tr/td/table[@width="100%"]'
    mvsearch_list = etree_html.xpath(mvsearch_xpath)
    # print(mvsearch_list)

    if len(mvsearch_list) == 0:
        print("未搜索到任何内容")
        return -1

    # print("共找到", len(mvsearch_list), "个关于", mvsearch_name, "的结果:")

    mvcontent_url = []
    mvcontent_title = []

    # 提取搜索结果中的电影链接
    mvsearch_list_len = len(mvsearch_list)
    for idx in range(1, mvsearch_list_len+1):
        # 提取链接
        mv_title_url = etree_html.xpath(
            mvsearch_xpath + '[{0}]//a[@href]/@href'.format(idx))
        # print(mv_title_url)

        if mv_title_url == None:
            print("解析出错!")
            return -1

        # 过滤掉游戏
        if mv_title_url[0].find("/html/game/") < 0:
            mv_title_url = "{0}{1}".format(MOVIE_URL, mv_title_url[0])
            mvcontent_url.insert(idx-1, mv_title_url)
            # 提取标题
            mv_title_str_lst = etree_html.xpath(
                mvsearch_xpath + '[{0}]//a[@href]//text()'.format(idx))
            if mv_title_str_lst == None:
                print("解析出错!")
                return -1
            mv_title_str = "".join(mv_title_str_lst)
            mvcontent_title.insert(idx-1, mv_title_str)
            # print("\t{0}, {1}, {2}".format(idx, mv_title_str, mv_title_url))

    # print(mvcontent_url)
    # print(mvcontent_title)

    mvcontent_len = len(mvcontent_url)

    if mvcontent_len == 0:
        print("未搜索到有效结果!")
        return -1

    # print("其中", mvcontent_len, "个有效结果:")
    print("共找到", mvcontent_len, "个关于", mvsearch_name, "的下载:")
    for idx in range(mvcontent_len):
        print("\t", idx+1, ", ",
              mvcontent_title[idx], ", ", mvcontent_url[idx])

    # 打开电影详情页面
    mvcontent_sel = input("请选择需要下载的项:")
    if mvcontent_sel.isdigit() != True:
        print("输入有误!")
        return -1
    mvcontent_sel = int(mvcontent_sel)
    if mvcontent_sel > mvcontent_len or mvcontent_sel < 1:
        print("输入有误!")
        return -1
    mvcontent_sel = mvcontent_sel - 1

    # 下载电影详情页面
    # print("即将下载: ", mvcontent_title[mvcontent_sel],
    #       ", " + mvcontent_url[mvcontent_sel])
    mvcontent_html = download_page_html(mvcontent_url[mvcontent_sel], 1)
    # print(mvcontent_html)

    if mvcontent_html == None:
        print("下载出错,可能IP被服务器封禁,可稍后再试!")
        return -1

    # 提取电影下载链接
    mvcontent_etree_html = lxml.html.fromstring(mvcontent_html)
    # print(etree.tostring(mvcontent_etree_html, encoding="utf-8").decode("utf-8"))

    # '//div[@id="Zoom"]/table/tr/td/table'
    mvcontent_xpath = '//td[@bgcolor="#fdfddf"]'

    mvcontent_dwurl_lst = []

    mvcontent_urllst = mvcontent_etree_html.xpath(
        mvcontent_xpath + "//a[@href]/text()")
    if mvcontent_urllst == None:
        print("解析出错!")
        return -1

    for url in mvcontent_urllst:
        mvcontent_dwurl_lst.append(url)

    if mvcontent_dwurl_lst == None:
        print("未找到下载链接!")
        return -1

    # print("共找到", len(mvcontent_dwurl_lst), "个下载链接:")

    for dwurl in mvcontent_dwurl_lst:
        print("\t", dwurl)

    return 0


def movie_douban(mvsearch_name):
    DOUBANMV_SEARCH_URL = "https://movie.douban.com/j/subject_suggest"
    DOUBANMV_SEARCH_PAR = {"q": ""}
    # mvsearch_name = "星际迷航"

    if mvsearch_name == None:
        print("输入有误！")
        return -1
    
    print("正在从豆瓣电影搜索", mvsearch_name)

    DOUBANMV_SEARCH_PAR["q"] = mvsearch_name

    # url参数编码
    mvsearch_par = parse.urlencode(DOUBANMV_SEARCH_PAR, encoding="utf-8")
    # print(mvsearch_par)
    mvsearch_url = "{0}?{1}".format(DOUBANMV_SEARCH_URL, mvsearch_par)
    # print(mvsearch_url)

    # 下载指定url
    mvsearch_html = download_page_html(mvsearch_url, 2)
    if mvsearch_html == None:
        print("下载出错,可能IP被服务器封禁,可稍后再试!")
        return -1

    # 解析下载的结果(json格式)
    try:
        mvsearch_json = json.loads(mvsearch_html)
    except json.JSONDecodeError as e:
        print("出现错误:", e)
        return -1

    if mvsearch_json == None or len(mvsearch_json) == 0:
        print("未找到相关结果!")
        return -1
    # print(mvsearch_json)

    # 输出解析结果
    print("共找到", len(mvsearch_json), "个关于", mvname, "的结果: ")
    for i in range(len(mvsearch_json)):
        print("\t", i+1, mvsearch_json[i]["title"],
              "/", mvsearch_json[i]["sub_title"])

    # 选择需要查看的项
    search_sel = input("请选择需要查看的项:")
    if search_sel.isdigit() != True:
        print("输入有误!")
        return -1
    search_sel = int(search_sel)
    if search_sel > len(mvsearch_json) or search_sel < 1:
        print("输入有误!")
        return -1
    search_sel = search_sel - 1

    # 获取需要查看的项的url,下载需要查看的项
    mvcontent_url = mvsearch_json[search_sel]["url"]
    mvcontent_html = download_page_html(mvcontent_url, 2)

    # 解析需要查看的项
    doubanmv_etree_html = lxml.html.fromstring(mvcontent_html)
    # print(type(doubanmv_etree_html))
    # print(etree.tostring(doubanmv_etree_html, encoding="utf-8").decode("utf-8"))
    mvcontent_xpath = '/html/head//script[@type="application/ld+json"]/text()'
    mvcontent_text = doubanmv_etree_html.xpath(mvcontent_xpath)
    if mvcontent_text == None or len(mvcontent_text) == 0:
        print("未找到相关结果")
        return -1

    mvcontent_text[0] = mvcontent_text[0].replace("\n", "")  # 替换掉json字符串中的\n
    # print(type(mvcontent_text), len(mvcontent_text))
    # print(mvcontent_text)
    try:
        mvcontent_json = json.loads(mvcontent_text[0])
    except json.JSONDecodeError as e:
        print("解析出错:", e)
        return -1
    # print(type(mvcontent_json))
    # print(mvcontent_json)
    if mvcontent_json == None or len(mvcontent_json) == 0:
        print("未找到相关结果")
        return -1
    # print(type(mvcontent_json))

    # 输出电影详情
    print("\t电影名称", mvcontent_json["name"])

    # 合并显示电影类型
    mvcontent_genre = mvcontent_json["genre"]
    mvcontent_genre_str = ""
    for lst in mvcontent_genre:
        mvcontent_genre_str += (lst + "/")
    print("\t电影类型", mvcontent_genre_str)

    print("\t上映时间", mvcontent_json["datePublished"])
    print("\t豆瓣评分", mvcontent_json["aggregateRating"]["ratingValue"],
          "(", mvcontent_json["aggregateRating"]["ratingCount"], ")")
    print("\t电影导演", mvcontent_json["director"][0]["name"])
    # 合并显示电影主演(只显示前5个)
    mvcontent_actor = mvcontent_json["actor"]
    mvcontent_actor_str = ""
    mvcontent_actor_len = 0
    for lst in mvcontent_actor:
        mvcontent_actor_str += (lst["name"] + "/")
        mvcontent_actor_len += 1
        if mvcontent_actor_len > 5:
            mvcontent_actor_str += "..."
            break
    print("\t电影主演", mvcontent_actor_str)
    print("\t电影简述", mvcontent_json["description"])

    # if movie_tiantang(mvsearch_json[search_sel]["title"]) == -1:
    # return -1

    return 0


if __name__ == "__main__":
    while True:
        # mvname = "星际迷航"
        mvname = input("请输入电影名称(输入\"exit\"退出):")
        if mvname == None or len(mvname) == 0:
            continue
        if mvname == "exit":
            exit()
        if movie_douban(mvname) == -1:
            # exit()
            pass
        if movie_tiantang(mvname) == -1:
            # exit()
            pass
