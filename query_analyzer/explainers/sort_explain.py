from color import bold_string


def sort_explain(query_plan):
    result = "The result is sorted using the attribute "
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
