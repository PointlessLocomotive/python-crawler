#!/usr/local/bin/python
# -*- coding: utf-8-*-
import urllib


def get_candidate_info(candidate, conn, api):
    user = api.get_user(candidate["user_id"])
    cur = conn.cursor()

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
    conn.commit()
