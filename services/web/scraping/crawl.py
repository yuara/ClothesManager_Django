import os
import scrapy
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from billiard import Process
from scraping.scraping.spiders.forecast import ForecastSpider
from scraping.scraping import settings


# class UrlCrawlerScript(Process):
#     def __init__(self, spider):
#         Process.__init__(self)
#         settings = get_project_settings()
#         self.crawler = Crawler(settings)
#         self.crawler.configure()
#         self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
#         self.spider = spider
#
#     def run(self):
#         self.crawler.crawl(self.spider)
#         self.crawler.start()
#         reactor.run()


def run_spider():
    process = CrawlerProcess(
        settings={
            "ROBOTSTXT_OBEY": True,
            "DOWNLOAD_DELAY": 3,
            "ITEM_PIPELINES": {"scraping.scraping.pipelines.ForecastPipeline": 300,},
            "POSTGRES_URL": os.environ.get("POSTGRES_URL"),
        }
    )
    process.crawl(ForecastSpider)
    process.start()
    # crawler.join()
