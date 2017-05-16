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
        # <div class="l_post j_l_post l_post_bright " data-field="
        #   {"author":{"user_id":2822234658,
        #   "user_name":"\u6e29\u67d4\u88ab\u8986\u706d",
        #   "name_u":"%E6%B8%A9%E6%9F%94%E8%A2%AB%E8%A6%86%E7%81%AD&ie=utf-8",
        #   "user_sex":2,"portrait":"22e2e6b8a9e69f94e8a2abe8a686e781ad37a8",
        #   "is_like":1,"level_id":6,"level_name":"\u5ba0\u7269\u77e5\u5df1",
        #   "cur_score":114,"bawu":0,"props":null},
        #   "content":{"post_id":106027375899,"is_anonym"   **********
        # <div class="user-hide-post-position"></div>
        # <div class="d_author">
        # <div class="d_post_content_main">
        # <div class="p_content p_content p_content_nameplate">
        # <div class="save_face_bg_hidden save_face_bg_0">
        # <cc>
            # <div id="post_content_106027375899"
            # class="d_post_content j_d_post_content clearfix"> 四个月柯基耳朵有点发炎 导致那边耳朵不立怎么办。。</div>
            # <br>
        # </cc>
        # patten = re.compile(r'<div class="l_post.*?data-field.*?user_name":"(.*?)","name_u.*?' +
        #                     r'level_name":"(.*?)","cur_score.*?' +
        #                     r'<div id="post_content_.*?">(.*?)</div', re.S)
        # data = re.search(patten, source)
        # if data:
        #     print data.group(1), data.group(2), data.group(3)
        #     return data.group(1).strip(), data.group(2).strip(), data.group(3).strip()
        # else:
        #     return None


        patten = re.compile(r'level_name":"(.*?)".*?' +
                            r'<div id="post_content_.*?">(.*?)</div', re.S)
        data = re.search(patten, source)
        if data:
            print data.group(1), data.group(2)
            return data.group(1).strip()
        else:
            return None

if __name__ == '__main__':
    working_url = 'http://tieba.baidu.com/p/3824525683'
    baidu_tieba = BaiduTieba(working_url)
    page_source = baidu_tieba.get_page_source(1)
    baidu_tieba.get_page_title(page_source)
    baidu_tieba.get_page_num(page_source)
    baidu_tieba.get_content(page_source)


