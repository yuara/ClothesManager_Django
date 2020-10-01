from scrapy.crawler import CrawlerProcess
from scraping.scraping.spiders.forecast import ForecastSpider


def run_spider():
    process = CrawlerProcess(
        settings={
            "ROBOTSTXT_OBEY": True,
            "DOWNLOAD_DELAY": 3,
            "ITEM_PIPELINES": {"scraping.scraping.pipelines.ForecastPipeline": 300,},
        }
    )
    process.crawl(ForecastSpider)
    process.start(stop_after_crawl=False)
