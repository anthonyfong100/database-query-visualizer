from os import error
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

    res = {"bounds": [], "query": query, "error": False, "err_msg": ""}

    if not len(query):
        res["error"] = True
        res["err_msg"] = "Empty query detected."

    for column in columns:
        table = query_runner.find_table(column)
        temp_bounds = query_runner.find_bounds(column)
        valid_col = query_runner.is_col_numeric(table, column)

        if not table:
            res["error"] = True
            return res

        if not valid_col:
            res["error"] = True
            res["err_msg"] = (
                "Invalid query. Column {} is non-numeric and cannot be varied."
            ).format(column)
            return res

        # create buckets using min max
        if not temp_bounds and table:
            temp_bounds = query_runner.find_alt_partitions(table, column)
            res["bounds"].append(temp_bounds)
            continue

        res["bounds"].append(temp_bounds)

    return res
