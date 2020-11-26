def aggregate_explain(query_plan):
    # For plans of the aggregate type: SortAggregate, HashAggregate, PlainAggregate
    strategy = query_plan["Strategy"]
    if strategy == "Sorted":
        result = "The rows are sorted based on their keys."
        if "Group Key" in query_plan:
            result += " They are grouped by the following keys: "
            for key in query_plan["Group Key"]:
                result += key + ","
            result += "."
        if "Filter" in query_plan:
            result += " They are filtered by " + query_plan["Filter"].replace(
                "::text", ""
            )
            result += "."
        return result
    elif strategy == "Hashed":
        result = "It hashes all rows based on the following key(s): "
        for key in query_plan["Group Key"]:
            result += key.replace("::text", "") + ", "
        result += "which are then put into bucket given by the hashed key."
        return result
    elif strategy == "Plain":
        return "Result is simply aggregated as normal."
    else:
        raise ValueError(
            "Aggregate_explain does not work for strategy: " + strategy
        )
