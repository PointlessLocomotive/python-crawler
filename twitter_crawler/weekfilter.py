import psycopg2
conn = psycopg2.connect(
    database='pointloc',
    user='pointloc',
    password='pointloc',
    host='10.40.60.191',
    port="5432"
)
cur = conn.cursor()
weeks =[
('20170303'),
 ('20170303','20170315'),
 ('20170316','20170322'),
 ('20170323','20170329'),
 ('20170330','20170406'),
 ('20170407','20170418'),
 ('20170419','20170420'),
 ('20170421','20170427'),
 ('20170428','20170503'),
 ('20170504','20170510'),
 ]
def week_filter(wn, con=cur):
    if(wn >= len(weeks) or wn < 0):
        err_ms ="week index can't be greater than " + str(len(weeks)-1) + " and less than 0"
        raise ReferenceError(err_ms)

    dates = weeks[wn]
    query = ("select text_analysis from tweets"
    " where created_at >= '%s'"
    " AND created_at <= '%s';")
    values =dates
    if(wn==0):
        query = ("select text_analysis from tweets"
        " where created_at < '%s';")
    con.execute(query % values)

    rows = con.fetchall()
    #print rows
    return rows

def candidate_week_filter(wn, can, con=cur):
    if(wn >= len(weeks) or wn < 0):
        err_ms ="week index can't be greater than " + str(len(weeks)-1) + " and less than 0"
        raise ReferenceError(err_ms)

    query = ("select candidate_id from candidates where screen_name = '%s';")
    con.execute(query % can)
    candidate_id =con.fetchall()[0]
    dates = weeks[wn]
    
    query = ("select text_analysis from tweets"
    " where created_at >= '%s'"
    " AND created_at <= '%s'"
    "AND author_id='%s';")
    values =dates+candidate_id
    if(wn==0):
        query = ("select text_analysis from tweets"
        " where created_at < '%s'"
        "AND author_id='%s';")

    con.execute(query % values)

    rows = con.fetchall()
    print rows[0]
    return rows


candidate_week_filter(5, "JosefinaVM")
