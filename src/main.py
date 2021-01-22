

#  MIT License
#
#  Copyright (c) 2021 Jinho Ko
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.


import os
import sys

import ibm_db as db
import sqlparse

DB2_IP = "0.0.0.0"
DB2_PORT = 50000
DB2_PROTOCOL = "TCPIP"
DB2_AUTHENTICATION = "SERVER"
DB2_USER = "db2inst1"
DB2_PASSWORD = "0000"

DB2_OPTIMIZE_LEVEL = 3 # integer between 1~9
DB2_DBNAME = "imdb"
DB2_DBSCHEMA = "DB2INST1"


def connectDB():

    conn = db.connect(f'DATABASE={DB2_DBNAME};'
                      f'HOSTNAME={DB2_IP};'
                      f'PORT={DB2_PORT};'
                      f'PROTOCOL={DB2_PROTOCOL};'
                      f'AUTHENTICATION={DB2_AUTHENTICATION};'
                      f'UID = {DB2_USER};'
                      f'PASSWORD={DB2_PASSWORD}', '', ' ')

    return conn


if __name__ == "__main__":

    conn = connectDB()

    setExplainModeSQL = "SET CURRENT EXPLAIN MODE EXPLAIN;"
    setNormalModeSQL = "SET CURRENT EXPLAIN MODE NO;"
    setOptimizeLevelSQL = f"SET CURRENT QUERY OPTIMIZATION {DB2_OPTIMIZE_LEVEL};"

    getRewrittenQuerySQL = "SELECT STATEMENT_TEXT FROM SYSTOOLS.EXPLAIN_STATEMENT ORDER BY EXPLAIN_TIME DESC LIMIT 1;"

    queryForRewriteSQL = """
        SELECT A.name FROM actor A JOIN cast C on A.aid = C.aid JOIN movie M on C.msid = M.mid WHERE M.title IN (SELECT M_IN.title FROM actor A_IN JOIN cast C_IN on A_IN.aid = C_IN.aid JOIN movie M_IN on C_IN.msid = M_IN.mid WHERE A_IN.name = 'Shawn Alfaro' )
    """

  #  queryForRewriteSQL = "SELECT * FROM actor A;"

    try:
        stmt = db.exec_immediate(conn, setOptimizeLevelSQL)
        stmt = db.exec_immediate(conn, setExplainModeSQL)
        stmt = db.exec_immediate(conn, queryForRewriteSQL)
        stmt = db.exec_immediate(conn, setNormalModeSQL)
        stmt = db.exec_immediate(conn, getRewrittenQuerySQL)
        queriedRow = db.fetch_assoc(stmt)
        rewrittenQueryText = queriedRow['STATEMENT_TEXT']
        rewrittenQueryTextWithHiddenSchema = rewrittenQueryText.replace(f"{DB2_DBSCHEMA}.", "")

        prettifiedSQL = sqlparse.format(rewrittenQueryTextWithHiddenSchema, reindent=True, keyword_case='upper')
        print(prettifiedSQL)

    except Exception as e:
        print(e)
    finally:
        db.close(conn)


