from query_analyzer.explainers.color import bold_string


def setop_explain(query_plan):
    # https://www.depesz.com/2013/05/19/explaining-the-unexplainable-part-4/
    result = "It finds the "
    cmd_name = bold_string(str(query_plan["Command"]))
    if cmd_name == "Except" or cmd_name == "Except All":
        result += "differences "
    else:
        result += "similarities "
    result += "between the two previously scanned tables using the {} operation.".format(
        bold_string(query_plan["Node Type"])
    )

    return result
