select customer_id, email
from {{ ref('silver_customers') }}
where email <> lower(trim(email))