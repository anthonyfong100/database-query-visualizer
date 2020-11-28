import os
import re

# import postgresql
from psycopg2 import connect, sql


# TODO: FIX THIS TO USE queryrunner instance to run commands
def findBounds(query):
    conn = connect(
        dbname=os.getenv("POSTGRES_DBNAME"),
        user=os.getenv("POSTGRES_USERNAME"),
        # password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )
    cur = conn.cursor()

    columns = []

    # Replace all occurences of VARY(X) with x < $i, where i is the placeholder counter
    while query.find("VARY") != -1:
        start = query.find("VARY(")
        subStr = query[start:]
        end = subStr.find(")")
        res = subStr[5:end] + " < (%f)"
        columns.append(subStr[5:end])
        query = query[:start] + res + query[start + end + 1 :]

    bounds = []

    for column in columns:
        # Find table names that the columns can be found in
        findTableQuery = sql.SQL(
            """
            SELECT t.table_schema, t.table_name FROM information_schema.tables t
            inner join information_schema.columns c on c.table_name = t.table_name
            and c.table_schema = t.table_schema where c.column_name = %s
            and t.table_schema not in ('information_schema', 'pg_catalog')
            and t.table_type = 'BASE TABLE' order by t.table_schema;
            """
        )

        cur.execute(findTableQuery, [column])

        res = cur.fetchall()

        # Nothing found
        if len(res) == 0:
            continue
        table = res[0][1]

        oldLevel = conn.isolation_level
        conn.set_isolation_level(0)
        analyzeQuery = sql.SQL(
            """
            VACUUM ANALYZE {queryTable} ({queryColumn});
            """
        ).format(
            queryTable=sql.Identifier(table),
            queryColumn=sql.Identifier(column),
        )

        cur.execute(analyzeQuery)
        conn.set_isolation_level(oldLevel)

        # analyze column with psycopg2
        col_query = (
            "select * from pg_stats where tablename='{}' and attname='{}'"
        ).format(table, column)
        cur.execute(col_query)
        analyze_fetched = cur.fetchall()[0]

        # separate histogram bounds from pg_stats into 10 buckets
        temp_bounds = []
        print(analyze_fetched[9])
        if not analyze_fetched[9]:
            continue

        full_bounds = analyze_fetched[9][1:-1].split(",")
        inc = len(full_bounds) // 10
        for i in range(inc, len(full_bounds), inc):
            temp_bounds.append(full_bounds[i])

        bounds.append(temp_bounds)

    # return {bounds: bounds, query: query}
    print(bounds)
    return bounds
