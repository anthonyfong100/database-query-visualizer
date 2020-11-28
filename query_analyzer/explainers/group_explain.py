def group_explain(query_plan):
    result = "The result from the previous operation is grouped together using the following keys "
    for i, key in enumerate(query_plan["Group Key"]):
        result += key.replace("::text", "")
        if i==len(query_plan["Group Key"])-1:
            result+="."
        else:
            result+=", "
    return result
