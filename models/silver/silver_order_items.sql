select order_item_id, order_id, product_id, quantity, 
unit_price,loaded_at from {{ ref('bronze_order_items') }}
where order_item_id is not null and quantity > 0