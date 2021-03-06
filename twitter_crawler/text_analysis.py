import json
import re
import os
import psycopg2

import indicoio


class TextAnalysis:
    def __init__(self):
        indicoio.config.api_key = os.environ['INDICO_KEY']
        self.conn = psycopg2.connect(
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS'],
            host=os.environ['DB_HOST'],
            port="5432"
        )

    @staticmethod
    def clean_text(text):
        text = text.replace('RT', '').replace('#', '').replace('@', '')

        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )

        if re.match(regex, text, 0):
            text = ""
        text = result = re.sub(r"http\S+", "", text)
        return text

    def get_text_analysis(self):
        cur = self.conn.cursor()
        query = (
            "SELECT tweet_id, text FROM tweets "
            "WHERE text_analysis::text='{}'::text;"
        )
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            text = row[1]
            text = self.clean_text(text)
            id = row[0]
            try:
                analysis = indicoio.analyze_text(
                    text,
                    apis=['sentiment',  'political', 'keywords', 'text_tags']
                )
                json_analysis = json.dumps(analysis)
                # print("analysing")
                query = "update tweets set text_analysis=%s where tweet_id=%s;"
                cur.execute(query, (json_analysis, id))
                self.conn.commit()
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message

                print "Error with tweet. Id: " + id + " text: " + text
                if ex.args[0] == 'Input contains one or more empty strings.':
                    query = "delete from tweets where tweet_id='%s';" % id
                    cur.execute(query)
                    self.conn.commit()
                    print('tweet deleted, text= ' + text)
        print "done indico analysis"
