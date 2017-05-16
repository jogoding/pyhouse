#!/usr/bin/python
# -*- encoding:utf-8 -*-
import urllib2
import re


class BaiduTieba:
    def __init__(self, url):
        self.base_url = url

        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        pass

    def get_page_source(self, page_num):
        try:
            url = self.base_url + "?pn=" + str(page_num)
            print url
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError, e:
            print u"Failed to connect Baidu Tieba.", e.message
            return None

    def get_page_title(self, source):
        # PageData.thread = {author:"蹦吧tua明明",thread_id :5073854136,title:"【晒日常】04-15丨东北人在苏州", reply_num:125,
        patten_title = re.compile(r'.*?PageData.*?author:"(.*?)".*?title:"(.*?)". reply', re.S)

        data = re.search(patten_title, source)
        if data:
            print data.group(1), data.group(2)
            return data.group(1).strip(), data.group(2).strip()
        else:
            return None

    def get_page_num(self, source):
        # <li class="l_reply_num" style="margin-left:8px" >
        # <span class="red" style="margin-right:3px">2540</span>回复贴，共
        # <span class="red">18</span>页</li>
        patten = re.compile(r'<li class="l_reply_num".*?<span.*?<span.*?>(.*?)</span')
        data = re.search(patten, source)
        if data:
            print data.group(1)
            return data.group(1).strip()
        else:
            return None
    def get_content(self, source):




if __name__ == '__main__':
    working_url = 'http://tieba.baidu.com/p/3824525683'
    baidu_tieba = BaiduTieba(working_url)
    page_source = baidu_tieba.get_page_source(1)
    baidu_tieba.get_page_title(page_source)
    baidu_tieba.get_page_num(page_source)

