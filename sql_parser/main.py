import postgresql

def parse(query):

    db = postgresql.open("pq://postgres@127.0.0.1:5432/TPC-H")
    print(query)
    execute = db.prepare(query)
    print(execute())