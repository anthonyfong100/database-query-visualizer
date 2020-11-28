select
	o_orderpriority,
	count(*) as order_count
from
	orders
where
	o_totalprice :varies
	and exists (
		select
			*
		from
			lineitem
		where
			l_orderkey = o_orderkey
			and l_extendedprice :varies
	)
group by
	o_orderpriority
order by
	o_orderpriority

