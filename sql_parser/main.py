from query_analyzer.queryrunner import query_runner

# import postgresql
from psycopg2 import connect, sql


def parse(query):

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
        temp_bounds = query_runner.find_bounds(column)

        # create buckets using min max
        if not temp_bounds:
            continue

        bounds.append(temp_bounds)

    return bounds
