# NightOwl
24/7 AI Student Assistant for KSU. This web crawler scrapes pages on the kennesaw.edu domain to create a dataset of documents for use in developing a language model to answer questions and summarize results relevant to users of the KSU website. 

## Results so far:
After scraping 4000 pages on the kennesaw.edu domain, we've created a dataset consisting of millions of words. The words of highest frequency are listed below. Frequencies will be updated as more documents are scraped and processed.

```bash
Total words: 1898336   
Total documents: 4047  
Avg words per page: 469

30 most occurring words:
 1. students    : 26673
 2. faculty     : 18891
 3. ksu         : 18706
 4. kennesaw    : 17565
 5. resources   : 15657
 6. campus      : 14955
 7. university  : 14950
 8. student     : 14844
 9. state       : 13374
10. alumni      : 13330
11. research    : 11986
12. business    : 11527
13. community   : 11458
14. staff       : 11262
15. online      : 11079
16. information : 11063
17. education   : 10002
18. family      :  9572
19. current     :  9479
20. marietta    :  9430
21. friends     :  8798
22. parents     :  8639
23. 2024        :  8417
24. ga          :  8131
25. contact     :  7799
26. programs    :  7679
27. college     :  7061
28. visit       :  6524
29. apply       :  6314
30. financial   :  6258
```
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

### Creating a vocabulary

After creating the JSON file, you may create a vocabulary using the **clean.py** file in the **NightOwl** folder. Specify the desired file to clean and create a vocabulary for in the **clean.py** script, and run:

```bash
$ python clean.py
```

The script will output the vocabulary. You may edit the script to save data and use it how you like.

### Where's my data?

The results from **crawler.py** are stored in **ksucrawler/ksucrawler/spiders/ksudocs.json**, or whichever name you chose for your json file.

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

    # Number of pages to fetch before terminating crawler (should be increased after testing is done)
    # "CLOSESPIDER_PAGECOUNT" : 10,
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
