#bin/bash: 
import scrapy
from bili.items import BiliItem
import json
import datetime
import re

#print(today)

class BlSpider(scrapy.Spider):
    name = 'bili'
    allowed_domains = ['www.bilibili.com']

    start_urls = [
        'https://www.bilibili.com/v/popular/rank/all',
        'https://www.bilibili.com/v/popular/rank/guochuang',
        'https://www.bilibili.com/v/popular/rank/documentary',
        'https://www.bilibili.com/v/popular/rank/douga',
        'https://www.bilibili.com/v/popular/rank/music',
        'https://www.bilibili.com/v/popular/rank/dance',
        'https://www.bilibili.com/v/popular/rank/game',
        'https://www.bilibili.com/v/popular/rank/knowledge',
        'https://www.bilibili.com/v/popular/rank/tech',
        'https://www.bilibili.com/v/popular/rank/car',
        'https://www.bilibili.com/v/popular/rank/life',
        'https://www.bilibili.com/v/popular/rank/food',
        'https://www.bilibili.com/v/popular/rank/animal',
        'https://www.bilibili.com/v/popular/rank/kichiku',
        'https://www.bilibili.com/v/popular/rank/fashion',
        'https://www.bilibili.com/v/popular/rank/ent',
        'https://www.bilibili.com/v/popular/rank/cinephile'
                  ]

    def parse(self, response):
        #获取当前爬取的榜单名字，使用要注意正则匹配规则
        rank_tab=response.xpath('//ul[@class="rank-tab"]/li[@class="rank-tab--active"]/text()').getall()[0]
        print('='*50,'当前爬取榜单为:',rank_tab,'='*50)
        #之后遍历rank_lists获取每个视频的信息
        rank_lists=response.xpath('//ul[@class="rank-list"]/li')
        for rank_list in rank_lists:
            rank_num=rank_list.xpath('div[@class="num"]/text()').get()
            title=rank_list.xpath('div/div[@class="info"]/a/text()').get()
            title = ''.join(re.findall(r'[\u4e00-\u9fa5]',title))
            # 抓取视频的url，切片后获得视频的id
            id=rank_list.xpath('div/div[@class="info"]/a/@href').get().split('/BV')[-1]
            id = "BV" +id
            # 拼接详情页api的url
            #https://api.bilibili.com/x/web-interface/view?bvid=
            Detail_link='https://api.bilibili.com/x/web-interface/view?bvid={}'.format(id)
            Labels_link='https://api.bilibili.com/x/tag/archive/tags?bvid={}'.format(id)            
            author=rank_list.xpath('div/div[@class="info"]/div[@class="detail"]/a/span/text()').get()
            author =author.strip()
            author = author.strip("\"")
            author = ''.join(re.findall(r'[\u4e00-\u9fa5]',author))
            score=rank_list.xpath('div/div[@class="info"]/div[@class="pts"]/div/text()').get()
            # 这里创建一个字典去储存我们已经抓到的数据
            # 如果这里直接给到Scrapy的Item的话，最后排行页的数据会有缺失
            items={
                'rank_tab':rank_tab,
                'rank_num' : rank_num ,
                'title' :title ,
                'id' : id ,
                'author' : author ,
                'score' : score ,
                'Detail_link':Detail_link
            }
            # 将api发送给调度器进行详情页的请求，通过meta传递排行页数据
            yield scrapy.Request(url=Labels_link,callback=self.Get_labels,meta={'item':items},dont_filter=True)

    def Get_labels(self,response):
        items=response.meta['item']
        Detail_link=items['Detail_link']
        # 解析json数据
        #3.6才支持直接导入二进制，无需编码成utf-8
        html=json.loads(response.body.decode('utf-8'))
        #json.loads(html.decode('utf-8'))
        Tags=html['data'] #视频标签数据
        tag_name='-'.join([i['tag_name'] for i in Tags])
        #tag_name= ''.join(re.findall(r'[\u4e00-\u9fa5]',tag_name))
        items['tag_name']=tag_name
        yield scrapy.Request(url=Detail_link,callback=self.Get_detail,meta={'item':items},dont_filter=True)

    def Get_detail(self,response):
        # 获取排行页数据
        items=response.meta['item']
        rank_tab=items['rank_tab']
        rank_num=items['rank_num']
        title=items['title']
        id=items['id']
        author=items['author']
        score=items['score']
        tag_name=items['tag_name']

        # 解析json数据
        html=json.loads(response.body.decode('utf-8'))

        # 获取详细播放信息,二级json
        stat1=html['data']['stat']

        view=stat1['view']
        danmaku =stat1['danmaku']
        reply =stat1['reply']
        favorite =stat1['favorite']
        coin =stat1['coin']
        share =stat1['share']
        like =stat1['like']
        today = datetime.date.today()
        # 把所有爬取的信息传递给Item
        item=BiliItem(
            time = today,
            rank_tab=rank_tab,
            rank_num = rank_num ,
            title = title ,
            id = id ,
            author = author ,
            score = score ,
            view = view ,
            danmaku = danmaku ,
            reply = reply ,
            favorite = favorite ,
            coin = coin ,
            share = share ,
            tag_name = tag_name ,
            like = like
        )
        yield item
