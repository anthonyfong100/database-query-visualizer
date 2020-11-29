from color import bold_string


def index_scan_explain(query_plan):
    result = ""
    result += "An index scan is done using an index table " + bold_string(
        query_plan["Index Name"]
    )
    if "Index Cond" in query_plan:
        result += " with the following conditions: " + bold_string(
            query_plan["Index Cond"].replace("::text", "")
        )
    result += ", and the {} table and fetches rows pointed by indices matched in the scan.".format(
        bold_string(query_plan["Relation Name"])
    )

    if "Filter" in query_plan:
        result += (
            " The result is then filtered by "
            + bold_string(query_plan["Filter"].replace("::text", ""))
            + "."
        )
    return result


def index_only_scan_explain(query_plan):
    result = ""
    result += "An index scan is done using an index table " + bold_string(
        query_plan["Index Name"]
    )
    if "Index Cond" in query_plan:
        result += " with condition(s) " + bold_string(
            query_plan["Index Cond"].replace("::text", "")
        )
    result += ". It then returns the matches found in index table scan as the result."
    if "Filter" in query_plan:
        result += (
            " The result is then filtered by "
            + bold_string(query_plan["Filter"].replace("::text", ""))
            + "."
        )

    return result
