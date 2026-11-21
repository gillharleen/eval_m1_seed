select customer_id, full_name, email, city, 
created_at as customer_since from {{ ref('silver_customers') }}