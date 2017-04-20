import unittest
import psycopg2
import os
import indicoio

from indico import get_text_analysis
from indico import clean_text


class TddInPointless(unittest.TestCase):

    def test_clean_text(self):
        text = "Alfredo del Mazo Maza, la gran derrota del PRI https://t.co/KldihpHzvW"
        r = clean_text(text)
        res = "Alfredo del Mazo Maza, la gran derrota del PRI"
        print r
        self.assertEqual(r, res)

    # def test_get_text_analysis(self):
    #     indicoio.config.api_key = '98b26a72259df5f8df1f280747a6f6d6'

    #     conn = psycopg2.connect(
    #      database=os.environ['DB_NAME'],
    #      user=os.environ['DB_USER'],
    #      password=os.environ['DB_PASS'],
    #      host=os.environ['DB_HOST'],
    #      port="5432")

    #     get_text_analysis(conn, indicoio)
    #     self.assertEqual(4,4)


if __name__ == '__main__':
    unittest.main()
