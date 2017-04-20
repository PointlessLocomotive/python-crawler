#!/usr/local/bin/python
# -*- coding: utf-8-*-
import os
import time
import json

import psycopg2
import tweepy


import settings
settings.load_settings('dev')

from getCandidateInfo import get_candidate_info
from getFollowers import get_followers
from getSearch import get_hash_tags
from getTweets import get_tweets
from indico import get_text_analysis
from settings import load_settings


consumer_key = os.environ['TWITTER_KEY']
consumer_secret = os.environ['TWITTER_SECRET']
access_token = os.environ['TWITTER_TOKEN']
access_token_secret = os.environ['TWITTER_TOKEN_SECRET']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(
    auth_handler=auth,
    wait_on_rate_limit_notify=True,
    wait_on_rate_limit=True
)

conn = psycopg2.connect(
    database=os.environ['DB_NAME'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS'],
    host=os.environ['DB_HOST'],
    port="5432"
)

candidates = json.load(open('candidates.json'))

print "Opened database successfully"

for candidate in candidates:
        print " === current candidate: " + candidate["screen_name"] + " === "
        get_candidate_info(candidate, conn, api)
        print "all candidate info saved"
        get_tweets(candidate, conn, api)
        print("all candidate teweets saved")
        for word in candidate["key_words"]:
                get_hash_tags(word, conn, api)
print "done"

get_text_analysis(conn)

