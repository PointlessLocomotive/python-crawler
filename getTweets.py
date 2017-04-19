import tweepy
import psycopg2
import time
import os
import json

def get_tweets(user, conn, api):
    user = user["user_id"]
    userTweets = api.user_timeline(user_id=user, count=200, include_rts=True)
    for status in userTweets:

        mentions = json.dumps(status.entities['user_mentions'])
        cur = conn.cursor()
        query = "INSERT INTO tweets VALUES(%s, %s,%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (tweet_id) DO UPDATE SET favorites_number = excluded.favorites_number, retweets_number = excluded.retweets_number, replies_number = excluded.replies_number;"
        cur.execute(query, (status.id_str, status.user.id_str, status.text, mentions, status.favorite_count,status.retweet_count,0,"{}",status.created_at))
        conn.commit()

    print ("getting tweets done successfully")
