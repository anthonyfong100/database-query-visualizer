from query_analyzer.explainers.color import bold_string


def sort_explain(query_plan):
    result = f"The result is {bold_string('sorted')} using the attribute "
    if "DESC" in query_plan["Sort Key"]:
        result += (
            bold_string(str(query_plan["Sort Key"].replace("DESC", "")))
            + " in descending order"
        )
    elif "INC" in query_plan["Sort Key"]:
        result += (
            bold_string(str(query_plan["Sort Key"].replace("INC", "")))
            + " in increasing order"
        )
    else:
        result += bold_string(str(query_plan["Sort Key"]))
    result += "."
    return result
