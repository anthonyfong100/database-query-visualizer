def unique_explain(query_plan):
    result = "Using the sorted data from the sub-operations, a scan is done on each row and those with duplicated values are discarded."
    return result
