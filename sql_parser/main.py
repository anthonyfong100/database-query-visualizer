import postgresql
import re

def parse(query):

    db = postgresql.open("pq://postgres@127.0.0.1:5432/TPC-H")

    columns = []

    # Replace all occurences of VARY(X) with x < $i, where i is the placeholder counter
    count = 1
    while(query.find('VARY') != -1):
        start = query.find('VARY(')
        subStr = query[start:]
        end = subStr.find(')')
        res = subStr[5:end] + " < $" + str(count)
        columns.append(subStr[5:end])
        query = query[:start] + res + query[start + end + 1:]
        count += 1
        
    print(columns)
    queries = []
    
    # Find table names that the columns can be found in
    for column in columns:
        findTableQuery = "select t.table_schema, t.table_name from information_schema.tables t inner join information_schema.columns c on c.table_name = t.table_name and c.table_schema = t.table_schema where c.column_name = '" + column + "' and t.table_schema not in ('information_schema', 'pg_catalog') and t.table_type = 'BASE TABLE' order by t.table_schema;"
        execute = db.prepare(findTableQuery)
        # TODO: run analyze on each column
        print(execute())
    
    # TODO: using min and max values of each column, split into 10 buckets and generate 10 different queries
        