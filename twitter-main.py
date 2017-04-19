#!/usr/local/bin/python
# -*- coding: utf-8-*-
import tweepy
import psycopg2
import time
import os
import indicoio

from getFollowers import get_followers
from getCandidateInfo import get_candidate_info
from getTweets import get_tweets
from getSearch import get_hash_tags
from indico import get_text_analysis

indicoio.config.api_key = os.environ['INDICO_KEY']

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
    "user_id": '583488712',
    "screen_name": '@JuanZepeda_',
    "political_party":'PRD',
    "political_orientation": 'Izquierda',
    "key_words":'Juan Manuel Zepeda Hernández, JMZH, @JuanZepeda_, #JuanSiPuede'
  },
  {
    "user_id": '41421105',
    "screen_name": '@JosefinaVM',
    "political_party":'PAN',
    "political_orientation": 'Derecha',
    "key_words":'Josefina Vázquez Mota, JVM, @JosefinaVM, #MásQueUnCambio'
  },
  {
    "user_id": '3166004946',
    "screen_name": '@delfinagomeza',
    "political_party":'MORENA',
    "political_orientation": 'Izquierda',
    "key_words":'Delfina Gómez Álvarez, DGA, @delfinagomeza, #LaEsperanzaSeVota'
  },
  {
    "user_id": '198668037',
    "screen_name": '@OscarGonzalezYa',
    "political_party":'PRD',
    "political_orientation": 'Izquierda',
    "key_words":'Óscar González Yañez, OGY, @OscarGonzalezYa, #EstoyDeTuLado'
  },
 {
   "user_id": '39860797',
   "screen_name": '@alfredodelmazo',
   "political_party":'PRI',
   "political_orientation": 'Centro',
   "key_words":'Alfredo del Mazo Maza, AMM, @alfredodelmazo, #FuerteYconTodo'
 }


]


print ("Opened database successfully")
for candidate in candidates:
    print (" ***********************current candidate: "+ candidate["screen_name"]+ "*********************************")
    get_candidate_info(candidate, conn, api )
    print ("all candidate info saved")
    get_tweets(candidate,conn,api)
    print ("all candidate teweets saved")
    for word in candidate["key_words"].split(','):
        get_hash_tags(word, conn, api)
print ("finished")

get_text_analysis(conn, indicoio);
