from query_analyzer.explainers.color import bold_string


def cte_explain(query_plan):
    result = (
        "A CTE scan is performed on the table "
        + bold_string(str(query_plan["CTE Name"]))
        + " which is stored in memory "
    )
    if "Index Cond" in query_plan:
        result += " with condition(s) " + bold_string(
            query_plan["Index Cond"].replace("::text", "")
        )
    if "Filter" in query_plan:
        result += " and then filtered by " + bold_string(
            query_plan["Filter"].replace("::text", "")
        )
    result += "."
    return result


if __name__ == "__main__":
    test_cte_query_plan = {
        "CTE Name": "Test Name",
        "Index Cond": "Test Cond",
        "Filter": "Test Filter",
    }
    print(cte_explain(test_cte_query_plan))
