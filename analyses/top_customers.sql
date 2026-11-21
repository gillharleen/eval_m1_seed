-- Question: who are the highest-spending customers?
-- Uses: JOIN (fact to dim_customers) + aggregation + RANK window function.
select
    rank() over (order by sum(f.line_amount) desc) as spend_rank,
    c.full_name,
    c.city,
    count(distinct f.order_id) as orders,
    sum(f.line_amount)         as total_spent
from {{ ref('fct_orders') }} f
join {{ ref('dim_customers') }} c on c.customer_id = f.customer_id
where f.status <> 'cancelled'
group by c.customer_id, c.full_name, c.city
order by spend_rank, c.full_name