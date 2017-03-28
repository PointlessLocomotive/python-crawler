#!/usr/local/bin/python
# -*- coding: utf-8-*-
import tweepy
import psycopg2
import time
import os
from getFollowers import get_followers
from getCandidateInfo import get_candidate_info
from getTweets import get_tweets

consumer_key = os.environ['TWITTER_KEY']
consumer_secret = os.environ['TWITTER_SECRET']
access_token = os.environ['TWITTER_TOKEN']
access_token_secret = os.environ['TWITTER_TOKEN_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler = auth, wait_on_rate_limit_notify = True, wait_on_rate_limit=True)



conn = psycopg2.connect(
database=os.environ['DB_NAME'],
user=os.environ['DB_USER'],
password=os.environ['DB_PASS'],
host=os.environ['DB_HOST'],
port="5432")

candidates = [
    {
        "user_id": '41421105',
        "screen_name": 'JosefinaVM',
        "political_party":'PAN',
        "political_orientation": 'Derecha'
    },
    {
    "user_id": '3166004946',
    "screen_name": '@delfinagomeza',
    "political_party":'Morena',
    "political_orientation": 'Izquierda'
  },
  {
    "user_id": '39860797',
    "screen_name": '@alfredodelmazo',
    "political_party":'PRI',
    "political_orientation": 'Centro'
  },
  {
    "user_id": '407091449',
    "screen_name": '@IsidroPastor_',
    "political_party":'Independiente',
    "political_orientation": 'Desconocida'
  },
  {
    "user_id": '198668037',
    "screen_name": '@OscarGonzalezYa',
    "political_party":'PT',
    "political_orientation": 'Izquierda'
  },
  {
    "user_id": '583488712',
    "screen_name": '@JuanZepeda_',
    "political_party":'PRD',
    "political_orientation": 'Izquierda'
  }

]



print "Opened database successfully"
for candidate in candidates:
    get_candidate_info(candidate, conn, api )
    get_followers(candidate, conn, api )
    get_tweets(candidate,conn,api)
    #pass

cur = conn.cursor()
cur.execute("SELECT follower_id  from followers")
rows = cur.fetchall()
for row in rows:
    user = {}
    user['user_id'] = row[0]
    try:
        get_tweets(user,conn,api)
    except Exception:
        print Exception
        pass

conn.close()
