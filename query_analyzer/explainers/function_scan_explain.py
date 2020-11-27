def function_scan_explain(query_plan):
    parsed_plan = "The function {} is run and returns the recordset created by it.".format(query_plan["Function Name"])
    return parsed_plan