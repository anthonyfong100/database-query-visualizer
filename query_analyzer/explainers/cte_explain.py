def cte_explain(query_plan):
    result = "A CTE scan is performed on the table " + str(query_plan["CTE Name"]) + " which is stored in memory "
    if "Index Cond" in query_plan:
        result += " with condition(s) "+ query_plan["Index Cond"].replace('::text', '')
    if "Filter" in query_plan:
        result += " and then filtered by "+ query_plan["Filter"].replace('::text', '')
    result += "."
    