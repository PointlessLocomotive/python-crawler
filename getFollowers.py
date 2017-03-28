import tweepy
import psycopg2
import time
import os

def get_followers(candidate, conn, api):
    candidate = candidate["user_id"]
    follower_count = 0;
    for follower in limit_handled(tweepy.Cursor(api.followers,user_id=candidate).items()):
        follower_count = follower_count+1
        print follower_count
        if follower.friends_count < 200 and follower.default_profile_image == False:
            print follower.screen_name
            cur = conn.cursor()
            cur.execute("INSERT INTO followers values("+candidate+","+str(follower.id)+" ) ON CONFLICT DO NOTHING;")
            print "Operation done successfully";
            conn.commit()



def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)
