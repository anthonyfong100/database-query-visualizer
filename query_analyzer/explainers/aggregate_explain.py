from query_analyzer.explainers.color import bold_string


def aggregate_explain(query_plan):
    # For plans of the aggregate type: SortAggregate, HashAggregate, PlainAggregate
    strategy = query_plan["Strategy"]
    if strategy == "Sorted":
        result = "The rows are sorted based on their keys."
        if "Group Key" in query_plan:
            result += f" They are {bold_string('aggregated')} by the following keys: "
            for key in query_plan["Group Key"]:
                result += bold_string(key) + ","
            result = result[:-1]
            result += "."
        if "Filter" in query_plan:
            result += " They are filtered by " + bold_string(
                query_plan["Filter"].replace("::text", "")
            )
            result += "."
        return result
    elif strategy == "Hashed":
        result = "It hashes all rows based on the following key(s): "
        for key in query_plan["Group Key"]:
            result += bold_string(key.replace("::text", "")) + ", "
        result += f"which are then {bold_string('aggregated')} into bucket given by the hashed key."
        return result
    elif strategy == "Plain":
        return f"Result is simply {bold_string('aggregated')} as normal."
    else:
        raise ValueError(
            "Aggregate_explain does not work for strategy: " + strategy
        )


if __name__ == "__main__":
    test_aggregate_sorted_plan = {
        "Strategy": "Sorted",
        "Group Key": ["A", "B", "C"],
        "Filter": "Random Condition",
    }
    test_aggregate_hashed_plan = {
        "Strategy": "Hashed",
        "Group Key": ["A", "B", "C"],
    }

    print(aggregate_explain(test_aggregate_sorted_plan))
    print(aggregate_explain(test_aggregate_hashed_plan))
