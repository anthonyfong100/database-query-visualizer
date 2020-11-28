def hash_join_explain(query_plan):
    result = ""
    result += "The result from previous operation is joined using Hash {} Join".format(query_plan["Join Type"])
    if 'Hash Cond' in query_plan:
        result += " on the condition: {}".format(query_plan['Hash Cond'].replace("::text", ""))
    result += "."
    return result