from query_analyzer.explainers.color import bold_string


def group_explain(query_plan):
    result = f"The result from the previous operation is {bold_string('grouped')} together using the following keys: "
    for i, key in enumerate(query_plan["Group Key"]):
        result += bold_string(key.replace("::text", ""))
        if i == len(query_plan["Group Key"]) - 1:
            result += "."
        else:
            result += ", "
    return result
