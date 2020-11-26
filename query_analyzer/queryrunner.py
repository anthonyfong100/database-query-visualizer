import os
from typing import Any, Callable, List, Optional

import psycopg2

from query_analyzer.queryplan import QueryPlan


class QueryRunner:
    def __init__(self):
        self.conn = self.set_up_db_connection()
        self.cursor = self.conn.cursor()

    def set_up_db_connection(self):
        return psycopg2.connect(
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
