# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import thread
import time


#
class NjHouse:
    def __init__(self):
        self.page_index = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

        self.stories = []  # 存放段子的变量，每一个元素是每一页的段子们
        self.enable = False  # 存放程序是否继续运行的变量

    # 传入某一页的索引获得页面代码
    def get_page(self, page_index):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(page_index)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)

            # 存放程序是否继续运行的变量
            page_code = response.read().decode('utf-8')
            return page_code

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接糗事百科失败,错误原因", e.reason
                return None

    # 传入某一页代码，返回本页不带图片的段子列表
    def get_page_items(self, page_index):
        page_code = self.get_page(page_index)
        if not page_code:
            print "页面加载失败...."
            return None

        pattern = re.compile('<h2.*?h2>.*?<span>.*?</span>',
                             re.S)

        # pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)

        items = re.findall(pattern, page_code)

        page_stories = []
        for item in items:
            have_img = re.search("img", item[3])
            if not have_img:
                replace_br = re.compile('<br/>')
                text = re.sub(replace_br, "\n", item[1])
                # item[0]是一个段子的发布者，item[1]是内容，item[2]是发布时间,item[4]是点赞数
                page_stories.append([item[0].strip(), text.strip(), item[2].strip(), item[4].strip()])
        return page_stories

    # 加载并提取页面的内容，加入到列表中
    def load_page(self):
        if self.enable:
            if len(self.stories) < 2:
                page_stories = self.get_page_items(self.page_index)
                if page_stories:
                    self.stories.append(page_stories)
                    self.page_index += 1

    # 调用该方法，每次敲回车打印输出一个段子
    def get_one_story(self, page_stories, page):
        for story in page_stories:
            input_ = raw_input()
            self.load_page()
            if input_ == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t发布时间:%s\t赞:%s\n%s" % (page, story[0], story[2], story[3], story[1])

    # 开始方法
    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"

        self.enable = True
        self.load_page()
        current = 0

        #
        while self.enable:
            if len(self.stories) > 0:
                page_stories = self.stories[0]
                current += 1
                del self.stories[0]
                self.get_one_story(page_stories, current)


spider = NjHouse()
spider.start()
