def limit_explain(query_plan):
    # https://www.depesz.com/2013/05/09/explaining-the-unexplainable-part-3/
    result = "Instead of scanning the entire table, the scan is done with a limit of {} entries.".format(query_plan["Plan Rows"])
    return result