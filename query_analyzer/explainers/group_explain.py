def group_parser(query_plan):
    result = "The result from the previous operation is grouped together using the following keys "
    for i, key in enumerate(query_plan["Group Key"]):
        result += key.replace("::text", "")+", "
    result = result[:-2]
    result[-1]="."
    return result
