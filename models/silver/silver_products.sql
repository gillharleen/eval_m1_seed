select product_id, trim(product_name) as product_name, 
category, price from {{ ref('bronze_products') }}
where product_id is not null and price > 0