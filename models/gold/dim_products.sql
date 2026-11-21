select product_id, product_name, category,
price as list_price from {{ ref('silver_products') }}