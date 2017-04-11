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

        cur = conn.cursor()
        if (follower.friends_count/(follower.followers_count+1)) < 0.1 or follower.default_profile_image == False:
            print "FAKE: https://twitter.com/"+ follower.screen_name
            cur.execute("INSERT INTO followers values("+candidate+","+str(follower.id)+",FALSE ) ON CONFLICT DO NOTHING;")
            print "Operation done successfully";
            conn.commit()
        else:
            print "saved user: https://twitter.com/"+ follower.screen_name
            cur.execute("INSERT INTO followers values("+candidate+","+str(follower.id)+" ) ON CONFLICT DO NOTHING;")
            print "Operation done successfully";
            conn.commit()



def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)
