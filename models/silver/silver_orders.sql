select order_id, customer_id, 
order_date, {{ clean_text('status') }} as status, 
updated_at from {{ ref('bronze_orders') }}
where order_id is not null