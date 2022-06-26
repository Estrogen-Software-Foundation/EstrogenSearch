#!/usr/bin/python3 -B

import engineserver.crawler
import engineserver.indexdata

crawler = engineserver.crawler.WebCrawler()
crawler.scan_all()