def setop_explain(query_plan):
    # https://www.depesz.com/2013/05/19/explaining-the-unexplainable-part-4/
    result = "It finds the "
    cmd_name = str(query_plan["Command"])
    if cmd_name == "Except" or cmd_name == "Except All":
        result += "differences "
    else:
        result += "similarities "
    result += "between the two previously scanned tables using the {} operation.".format(query_plan["Node Type"])

    return result