import os
from typing import Any, Callable, List, Optional

from psycopg2 import connect, sql

from query_analyzer.queryplan import QueryPlan


class QueryRunner:
    def __init__(self):
        self.conn = self.set_up_db_connection()
        self.cursor = self.conn.cursor()

    def set_up_db_connection(self):
        return connect(
            dbname=os.getenv("POSTGRES_DBNAME"),
            user=os.getenv("POSTGRES_USERNAME"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
        )

    def tear_down_db_connection(self):
        self.conn.close()
        self.cursor.close()

    def explain(self, query: str) -> QueryPlan:
        self.cursor.execute("EXPLAIN (FORMAT JSON) " + query)
        plan = self.cursor.fetchall()
        query_plan_dict: dict = plan[0][0][0]["Plan"]
        return QueryPlan(query_plan_dict)

    def topKplans(
        self, plans: List[str], topK: int, **kwargs
    ) -> List[QueryPlan]:
        query_plans = [self.explain(plan) for plan in plans]
        return sorted(query_plans, **kwargs)[:topK]

    def find_table(self, column: str) -> str:
        # Find table names that the columns can be found in
        findTableQuery = sql.SQL(
            """
            SELECT t.table_schema, t.table_name FROM information_schema.tables t
            inner join information_schema.columns c on c.table_name = t.table_name
            and c.table_schema = t.table_schema where c.column_name = %s
            and t.table_schema not in ('information_schema', 'pg_catalog')
            and t.table_type = 'BASE TABLE' order by t.table_schema;
            """
        )

        self.cursor.execute(findTableQuery, [column])

        res = self.cursor.fetchall()

        # Nothing found
        if len(res) == 0:
            return None

        table = res[0][1]

        oldLevel = self.conn.isolation_level
        self.conn.set_isolation_level(0)
        analyzeQuery = sql.SQL(
            """
            VACUUM ANALYZE {queryTable} ({queryColumn});
            """
        ).format(
            queryTable=sql.Identifier(table),
            queryColumn=sql.Identifier(column),
        )

        self.cursor.execute(analyzeQuery)
        self.conn.set_isolation_level(oldLevel)

        return table

    def find_bounds(self, column: str) -> list:
        table = self.find_table(column)

        if not table:
            return None

        # analyze column with psycopg2
        col_query = (
            "select * from pg_stats where tablename='{}' and attname='{}'"
        ).format(table, column)
        self.cursor.execute(col_query)
        analyze_fetched = self.cursor.fetchall()[0]

        # separate histogram bounds from pg_stats into 10 buckets
        reduced_bounds = []
        full_bounds = analyze_fetched[9]

        # return None if no bounds found
        if not full_bounds:
            return None

        full_bounds = full_bounds[1:-1].split(",")
        inc = len(full_bounds) // 10
        for i in range(inc, len(full_bounds), inc):
            reduced_bounds.append(full_bounds[i])

        return reduced_bounds


query_runner = QueryRunner()
