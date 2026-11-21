-- Question: how does revenue build up day by day?
-- Uses: CTE + aggregation + running total (window function).
with daily as (
    select order_date, sum(line_amount) as revenue
    from {{ ref('fct_orders') }}
    where status <> 'cancelled'
    group by order_date
)
select
    order_date,
    revenue,
    sum(revenue) over (order by order_date) as running_revenue
from daily
order by order_date