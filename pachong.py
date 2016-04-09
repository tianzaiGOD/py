# encoding:utf-8
import urllib2
import re
import MySQLdb

conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='password',
    db='dbname',
    charset='utf8'
        )
cur = conn.cursor()
cur.execute("SET NAMES utf8")


class PaChong:

    def __init__(self):
        self.url = 'http://www.ccse.uestc.edu.cn/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/49.0.2593.0 Safari/537.36'}

    def catch_news(self):
        request = urllib2.Request(self.url, headers=self.headers)
        response = urllib2.urlopen(request)
        news = response.read()
        pattern = re.compile('<span><a\s\s\s*href="(.*?)".*?>.*?</span>', re.S)
        news_href = re.findall(pattern, news)
        i = 1
        for href in news_href:
            print i
            i = i + 1
            path = self.url + href
            request = urllib2.Request(path, headers=self.headers)
            response = urllib2.urlopen(request)
            infor = response.read()
            pattern = re.compile('<div.*?id="newsTitle".*?id="title".*?>(.*?)</p>.*?<div id="newsContent">(.*?)</div>', re.S)
            infor_href = re.search(pattern, infor).group(2)
            a = Tool().replace(infor_href)
            cur.execute("INSERT INTO pc VALUES (%s)", a)
            print a
        print('ok')
        conn.commit()
        conn.close()


class Tool:
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>|&nbsp;')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n",x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()


pachong = PaChong()
pachong.catch_news()
