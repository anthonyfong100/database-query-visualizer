def merge_join_explain(query_plan):
    result = "The results from sub-operations are joined using Merge Join"

    if 'Merge Cond' in query_plan:
        result += ' with condition ' + query_plan['Merge Cond'].replace("::text", "")

    if 'Join Type' == 'Semi':
        result += ' but only the row from the left relation is returned'
    
    result += '.'
    return result