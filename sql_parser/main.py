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

    res = {"bounds": [], "query": query, "error": False}

    for column in columns:
        table = query_runner.find_table(column)
        temp_bounds = query_runner.find_bounds(column)

        if not table:
            res["error"] = True
            return res

        # create buckets using min max
        if not temp_bounds and table:
            res["bounds"].append(
                query_runner.find_alt_partitions(table, column)
            )
            continue

        res["bounds"].append(temp_bounds)

    print(res)
    return res
