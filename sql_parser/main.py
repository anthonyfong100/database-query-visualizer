import postgresql
import psycopg2
import re


def parse(query):
    conn = psycopg2.connect("dbname=TPC-H user=postgres")
    cur = conn.cursor()
    # db = postgresql.open("pq://postgres@127.0.0.1:5432/TPC-H")

    columns = []

    # Replace all occurences of VARY(X) with x < $i, where i is the placeholder counter
    count = 1
    while query.find("VARY") != -1:
        start = query.find("VARY(")
        subStr = query[start:]
        end = subStr.find(")")
        res = subStr[5:end] + " < $" + str(count)
        columns.append(subStr[5:end])
        query = query[:start] + res + query[start + end + 1 :]
        count += 1

    print(columns)
    # queries = []

    bounds = []

    for column in columns:
        # Find table names that the columns can be found in
        findTableQuery = (
            "select t.table_schema, t.table_name from information_schema.tables t inner join information_schema.columns c on c.table_name = t.table_name and c.table_schema = t.table_schema where c.column_name = '"
            + column
            + "' and t.table_schema not in ('information_schema', 'pg_catalog') and t.table_type = 'BASE TABLE' order by t.table_schema;"
        )

        cur.execute(findTableQuery)
        table = cur.fetchall()[0][1]

        # analyze column with psycopg2
        col_query = (
            "select * from pg_stats where tablename='{}' and attname='{}'"
        ).format(table, column)
        cur.execute(col_query)
        analyze_fetched = cur.fetchall()[0]

        # separate histogram bounds from pg_stats into 10 buckets
        temp_bounds = []
        full_bounds = analyze_fetched[9][1:-1].split(",")
        inc = len(full_bounds) // 10
        for i in range(inc, len(full_bounds), inc):
            temp_bounds.append(full_bounds[i])

        bounds.append(temp_bounds)

    return bounds  # need to return list of queries also
