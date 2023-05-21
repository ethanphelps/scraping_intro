from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import sys

from wikiSpider.wikiSpider.items import Article

print(f'the number of modules in sys.modules is: {len(sys.modules)}')
print(sys.modules.keys())
print(f"sys.modules['wikiSpider'].__path__: {sys.modules['wikiSpider'].__path__}")
exit()

class ArticleSpider(CrawlSpider):
    name = 'articles'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
    rules = [Rule(LinkExtractor(allow=r'.*'),
                  callback='parse_items', follow=True)]

    def parse_items(self, response):
        article = Article()
        article['url'] = response.url
        article['title'] = response.css('h1 > span::text').extract_first()
        article['text'] = response.xpath('//div[@id="mw-content-text]"]//text()').extract()
        lastUpdated = response.css('li#footer-info-lastmod::text').extract_first()
        article['lastUpdated'] = lastUpdated.replace('This page was last edited on ', '')
        # print('URL is: {}'.format(url))
        # print('title is: {} '.format(title))
        # print('text is: {}'.format(text))
        # print('Last updated: {}'.format(lastUpdated))
        return article
