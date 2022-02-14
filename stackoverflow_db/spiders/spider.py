import scrapy
import json
import os
class My_Spider(scrapy.Spider):
    name = 'stack_spider'
    def start_requests(self):
        urls_list = []
        for i in range(0,30):
            urls_list.append("https://stackoverflow.com/questions?tab=newest&page="+str(i))
        urls = []
        urls.append("https://stackoverflow.com/questions")
        for i in range(0,len(urls_list)):
            urls.append(urls_list[i])
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        title_list = response.xpath("//div[@class = 's-post-summary--content']/h3/a/text()").extract()
        content_list = response.xpath("//div[@class = 's-post-summary--content-excerpt']/text()").extract()
        author_list = response.xpath("//div[@class = 's-user-card--link d-flex gs4']/a/text()").extract()
        link_list = response.xpath("//a[@class = 's-link']/@href").extract()

        tags_list = []
        for i in range(0, len(link_list)):
            str_tags = ""
            len_tags = len(response.xpath("/html/body/div[3]/div[2]/div[1]/div[3]/div["+ str(i+1) +"]/div[2]/div[2]/div[1]/a"))
            for j in range(0, len_tags):
                try:
                    str_tags += response.xpath("/html/body/div[3]/div[2]/div[1]/div[3]/div["+ str(i+1) +"]/div[2]/div[2]/div[1]/a[" + str(j+1) + "]/text()").extract()[0]
                except:
                    "none"
                finally:
                    str_tags += " "
            tags_list.append(str_tags)

        data = {}
        for i in range(0, len(link_list)):
            data[link_list[i]] = []
            data[link_list[i]].append({
                'title' : title_list[i],
                'content' : content_list[i],
                'author' : author_list[i],
                'tags' : tags_list[i]
            })
        with open('stack_overflow_db.txt', 'a+') as f:
            json.dump(data, f)
