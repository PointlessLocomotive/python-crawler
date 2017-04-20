import os
import time

import psycopg2
import tweepy


def get_followers(candidate, conn, api):
    candidate = candidate["user_id"]
    follower_count = 0
    tweepy_cursor = tweepy.Cursor(api.followers, user_id=candidate).items()
    for follower in limit_handled(tweepy_cursor):
        follower_count = follower_count + 1
        print follower_count

        cur = conn.cursor()
        friends_ratio = follower.friends_count / (follower.followers_count + 1)
        if friends_ratio < 0.1 or follower.default_profile_image is False:
            print "FAKE: https://twitter.com/%s" % follower.screen_name
            query = (
                "INSERT INTO followers VALUES(%s, %d, FALSE) "
                "ON CONFLICT DO NOTHING;" % (candidate, follower.id)
            )
            cur.execute(query)
            print "Operation done successfully"
            conn.commit()
        else:
            print "saved user: https://twitter.com/%s" % follower.screen_name
            query = (
                "INSERT INTO followers VALUES(%s, %d) "
                "ON CONFLICT DO NOTHING;" % (candidate, follower.id)
            )
            cur.execute(query)
            print "Operation done successfully"
            conn.commit()


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)
