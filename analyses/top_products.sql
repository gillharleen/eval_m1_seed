-- Question: which products sell best, by revenue and by units?
-- Uses: JOIN (fact to dim_products) + aggregation + RANK window function.
select
    p.product_name,
    p.category,
    sum(f.quantity)    as units_sold,
    sum(f.line_amount) as revenue,
    rank() over (order by sum(f.line_amount) desc) as revenue_rank
from {{ ref('fct_orders') }} f
join {{ ref('dim_products') }} p on p.product_id = f.product_id
where f.status <> 'cancelled'
group by p.product_id, p.product_name, p.category
order by revenue_rank