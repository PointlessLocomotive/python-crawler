""" Twitter Crawler module """
import os
import json
import psycopg2
import tweepy


class TwitterCrawler:
    """ Twitter Crawler class to fetch tweets based on candidates.json file """
    def __init__(self, candidates):
        auth = tweepy.OAuthHandler(
            os.environ['TWITTER_KEY'],
            os.environ['TWITTER_SECRET']
        )
        auth.set_access_token(
            os.environ['TWITTER_TOKEN'],
            os.environ['TWITTER_TOKEN_SECRET']
        )
        self.conn = psycopg2.connect(
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS'],
            host=os.environ['DB_HOST'],
            port="5432"
        )
        self.api = tweepy.API(
            auth_handler=auth,
            wait_on_rate_limit_notify=True,
            wait_on_rate_limit=True
        )
        self.candidates = json.load(open(candidates))

    @staticmethod
    def limit_handled(cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                time.sleep(15 * 60)

    def get_candidate_info(self, candidate):
        user = self.api.get_user(candidate["user_id"])
        cur = self.conn.cursor()

        firstInsert = (
            "INSERT INTO candidates VALUES (%s,%s,%s,%s,%s) "
            "ON CONFLICT (candidate_id) "
            "DO UPDATE SET candidate_id=excluded.candidate_id;"
        )
        values = (
            str(user.id),
            user.screen_name,
            candidate["political_party"],
            user.profile_image_url_https,
            candidate["political_orientation"]
        )
        secondInsert = (
            "INSERT INTO candidate_stats (candidate_id, follower_number) "
            "VALUES (%s, %d);" % (candidate["user_id"], user.followers_count)
        )
        cur.execute(firstInsert, values)
        cur.execute(secondInsert)
        print "Operation done successfully"
        self.conn.commit()

    def get_followers(self, candidate):
        candidate = candidate["user_id"]
        follower_count = 0
        tweepy_cursor = tweepy.Cursor(
            self.api.followers,
            user_id=candidate
        ).items()
        for follower in limit_handled(tweepy_cursor):
            follower_count = follower_count + 1
            print follower_count

            cur = self.conn.cursor()
            friends_ratio = follower.friends_count / (follower.followers_count + 1)
            if friends_ratio < 0.1 or follower.default_profile_image is False:
                print "FAKE: https://twitter.com/%s" % follower.screen_name
                query = (
                    "INSERT INTO followers VALUES(%s, %d, FALSE) "
                    "ON CONFLICT DO NOTHING;" % (candidate, follower.id)
                )
                cur.execute(query)
                print "Operation done successfully"
                self.conn.commit()
            else:
                print "saved user: https://twitter.com/%s" % follower.screen_name
                query = (
                    "INSERT INTO followers VALUES(%s, %d) "
                    "ON CONFLICT DO NOTHING;" % (candidate, follower.id)
                )
                cur.execute(query)
                print "Operation done successfully"
                self.conn.commit()

    def get_hash_tags(self, search):
        userTweets = self.api.search(q=search)

        for status in userTweets:
            mentions = json.dumps(status.entities['user_mentions'])
            cur = self.conn.cursor()
            query = (
                "INSERT INTO tweets VALUES(%s, %s,%s, %s, %s, %s, %s, %s, %s) "
                "ON CONFLICT (tweet_id) DO UPDATE SET "
                "favorites_number = excluded.favorites_number, "
                "retweets_number = excluded.retweets_number, "
                "replies_number = excluded.replies_number;"
            )
            values = (
                status.id_str,
                status.user.id_str,
                status.text,
                mentions,
                status.favorite_count,
                status.retweet_count,
                0,
                "{}",
                status.created_at
            )
            cur.execute(query, values)
            self.conn.commit()

        print "getting tweets done successfully"

    def get_tweets(self, user):
        user = user["user_id"]
        userTweets = self.api.user_timeline(
            user_id=user,
            count=200,
            include_rts=True
        )

        for status in userTweets:
            mentions = json.dumps(status.entities['user_mentions'])
            cur = self.conn.cursor()
            query = (
                "INSERT INTO tweets VALUES(%s, %s,%s, %s, %s, %s, %s, %s, %s) "
                "ON CONFLICT (tweet_id) DO UPDATE SET "
                "favorites_number = excluded.favorites_number, "
                "retweets_number = excluded.retweets_number, "
                "replies_number = excluded.replies_number;"
            )
            values = (
                status.id_str,
                status.user.id_str,
                status.text,
                mentions,
                status.favorite_count,
                status.retweet_count,
                0,
                "{}",
                status.created_at
            )
            cur.execute(query, values)
            self.conn.commit()

        print "getting tweets done successfully"
