import os
import scrapy
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from billiard import Process
from scraping.scraping.spiders.forecast import ForecastSpider
from scraping.scraping import settings


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
