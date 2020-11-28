from query_analyzer.queryrunner import query_runner


def parse(query):
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
        bounds.append(query_runner.fetch_bounds(column))

    return bounds

    # TODO need to return list of queries also
