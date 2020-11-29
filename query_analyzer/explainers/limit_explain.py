from query_analyzer.explainers.color import bold_string


def limit_explain(query_plan):
    # https://www.depesz.com/2013/05/09/explaining-the-unexplainable-part-3/
    result = f"Instead of scanning the entire table, the scan is done with a {bold_string('limit')} of {query_plan['Plan Rows']} entries."
    return result
