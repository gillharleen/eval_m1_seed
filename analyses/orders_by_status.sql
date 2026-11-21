-- Question: how many orders are in each status, and what are they worth?
-- Uses: aggregation only (no join needed).
select
    status,
    count(distinct order_id) as orders,
    count(*)                 as order_items,
    sum(line_amount)         as order_value
from {{ ref('fct_orders') }}
group by status
order by orders desc, status