from pathlib import Path
from bs4 import BeautifulSoup

import hashlib # Generate Unique Doc IDs from URLs
import scrapy

from scrapy.spiders import  Rule
from scrapy.linkextractors import LinkExtractor


class Ksucrawler(scrapy.Spider):
    name = "kennesaw_spider"
    allowed_domains = ["kennesaw.edu"]

    # TODO: Customize these settings
    custom_settings = {
        # Self identification
        "USER_AGENT" : "NLP @ KSU",

        # Wait before downloading consecutive pages
        "DOWNLOAD_DELAY" : 2,

        # FIFO/BFO: From https://doc.scrapy.org/en/latest/faq.html#does-scrapy-crawl-in-breadth-first-or-depth-first-order
        "DEPTH_PRIORITY" : 1,
        "SCHEDULER_DISK_QUEUE" : "scrapy.squeues.PickleFifoDiskQueue",
        "SCHEDULER_MEMORY_QUEUE" : "scrapy.squeues.FifoMemoryQueue",

        # TODO: Number of pages to fetch before terminating crawler (should be increased after testing is done)
        "CLOSESPIDER_PAGECOUNT" : 10,
    }

    # TODO: Add URLs if needed
    start_urls = [
        "https://www.kennesaw.edu/",
        'https://www.kennesaw.edu/faculty-staff/'
    ]

    # Define the rules for the spider
    rules = (
        Rule(LinkExtractor(allow=(), deny=(), unique=True), callback='parse_items', follow=True),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # Remove HTML tags from each document
        html = BeautifulSoup(response.body, "html.parser")
        for tag in html.find_all(True):
            tag.attrs = {}
        body = html.get_text()

        '''
        TODO: 
        if there is anything else we want to store, 
        create a rule and structure for that here. 
        For example, utilize regex to extract 
        emails and phone numbers.
        '''

        # Return results
        yield { 
            "pageid" : hashlib.md5(response.url.encode()).hexdigest(),
            "url" : response.url,
            "title" : response.css("title::text").get(),
            "body" : body,
            # TODO: additional document contents to extract, if wanted
        }

        # Iterate through links
        for link in LinkExtractor(allow=()).extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse, priority=1)