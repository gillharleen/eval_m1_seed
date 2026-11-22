select
    p.category,
    count(distinct f.order_id) as orders,
    sum(f.quantity)            as units_sold,
    sum(f.line_amount)         as revenue
from {{ ref('fct_orders') }} f
join {{ ref('dim_products') }} p on p.product_id = f.product_id
where f.status <> 'cancelled'
group by p.category, f.status
having f.status = 'completed'
order by revenue desc