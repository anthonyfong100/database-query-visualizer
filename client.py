import time

import psycopg2
from flask import Flask, redirect, render_template, request, url_for

from sql_parser.main import parse

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/result", methods=["POST", "GET"])
def explain():
    if request.method == "GET":
        return redirect("/")
    query = request.form["queryText"]
    parse(query)
    explanation = [
        "Anthony is a google intern",
        "Anthony is a fb intern",
        "Anthony is an apple intern",
    ]
    return render_template("index.html", query=query, explanation=explanation)


@app.route("/test_explain", methods=["GET"])
def test_explain():
    host = "localhost"
    port = "5432"
    dbname = "picasso"
    user = "postgres"
    password = "postgres"
    conn_string = "host='%s' port='%s' dbname='%s' user='%s' password='%s'" % (
        host,
        port,
        dbname,
        user,
        password,
    )
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    query = """select
    s_name,
    count(*) as numwait
from
    supplier,
    lineitem l1,
    orders,
    nation
where
    s_suppkey = l1.l_suppkey
    and o_orderkey = l1.l_orderkey
    and o_orderstatus = 'F'
    and exists (
        select
            *
        from
            lineitem l2
        where
            l2.l_orderkey = l1.l_orderkey
            and l2.l_suppkey <> l1.l_suppkey
    )
    and not exists (
        select
            *
        from
            lineitem l3
        where
            l3.l_orderkey = l1.l_orderkey
            and l3.l_suppkey <> l1.l_suppkey
            and l3.l_receiptdate > l3.l_commitdate
    )
    and s_nationkey = n_nationkey
    and n_name = 'SAUDI ARABIA'
group by
    s_name
order by
    numwait desc,
    s_name"""
    cursor.execute("EXPLAIN (FORMAT JSON) " + query)
    plan = cursor.fetchall()
    query_plan = plan[0][0][0]["Plan"]
    return query_plan


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
