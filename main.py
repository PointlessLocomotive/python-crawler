#!/usr/local/bin/python
# -*- coding: utf-8-*-
import json
from twitter_crawler import TwitterCrawler
from twitter_crawler import TextAnalysis
from twitter_crawler import load_settings

load_settings('dev')

candidates = json.load(open('candidates.json'))

crawler = TwitterCrawler('candidates.json')
tom = TextAnalysis()

for candidate in candidates:
    print " === current candidate: " + candidate["screen_name"] + " === "
    crawler.get_candidate_info(candidate, conn, api)
    print "all candidate info saved"
    crawler.get_tweets(candidate, conn, api)
    print("all candidate teweets saved")
    for word in candidate["key_words"]:
        crawler.get_hash_tags(word, conn, api)
    print "done"

tom.get_text_analysis(conn)
