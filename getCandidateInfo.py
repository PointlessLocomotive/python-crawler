#!/usr/local/bin/python
# -*- coding: utf-8-*-
#import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")

import urllib

def get_candidate_info(candidate, conn, api):
    user = api.get_user(candidate["user_id"])
    #print user._json
    cur = conn.cursor()

    firstInsert = "insert into candidates values (%s,%s,%s,%s,%s) ON CONFLICT (candidate_id) DO UPDATE set candidate_id=excluded.candidate_id;"

    secondInsert = "insert into candidate_stats (candidate_id, follower_number)  values ("+candidate["user_id"]+","+str(user.followers_count)+");"
    cur.execute(firstInsert,(str(user.id),user.screen_name, candidate["political_party"],user.profile_image_url_https,candidate["political_orientation"]))
    cur.execute(secondInsert)
    print ("Operation done successfully");
    conn.commit()
