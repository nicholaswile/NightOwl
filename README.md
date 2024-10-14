# NightOwl
24/7 AI Student Assistant for KSU. This web crawler scrapes pages on the kennesaw.edu domain to create a dataset of documents for use in developing a language model to answer questions and summarize results relevant to users of the KSU website. 

## How to run:

Clone this repository. If you haven't already, it is advised you create a virtual machine, and install the requirements for this project. You can do this by running
```bash
$ pip install -r requirements.txt
```

Then, to run the web crawler, change to the spiders directory, and use the scrapy commands. 
```bash
$ cd ksucrawler/ksucrawler/spiders
$ scrapy crawl -O ksudocs.json:json kennesaw_spider
```

The output of the crawler will be displayed in the json file. To create a new json file, specify it on the command line.

### Where's my data?

The results are stored in **ksucrawler/ksucrawler/spiders/ksudocs.json**, or whichever name you chose for your json file.

## How to modify:

The functionality of the crawler can be modified using the **crawler.py** script located in the **ksucrawler/ksucrawler/spiders folder**. Potential areas of modification include the following.

### Crawler settings

Potential settings to modify include how the agent identifies itself in HTTP requests, delay before downloading web pages, order of page exploration (depth first vs breadth first), number of pages crawled, etc.

```python
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
```

### Data extraction and storage

Currently HTML tags are removed, but there is still room for data processing. If we want to extract additional features like emails and phone numbers, we could add regular expressions after HTML tag removal.

```python
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
```

Then add the additional data to be stored in the yield statement, which includes the data saved after crawling is complete.

```python
yield { 
    "pageid" : hashlib.md5(response.url.encode()).hexdigest(),
    "url" : response.url,
    "title" : response.css("title::text").get(),
    "body" : body,
    # TODO: additional document contents to extract, if wanted
}
```

## Libraries and frameworks
* [Scrapy]("https://docs.scrapy.org/en/latest/intro/overview.html") for crawling web sites on the kennesaw.edu domain 
* [Beautiful Soup]("https://www.crummy.com/software/BeautifulSoup/bs4/doc/") for cleaning HTML tags

## Contributors
* Nicholas Wile
* Aidan Mitchell
<!--
* Afifa Jinan
--->
