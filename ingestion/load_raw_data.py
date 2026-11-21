import os
import random
from datetime import datetime, timedelta
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from faker import Faker

# Load values from the .env file in the project root (one folder above ingestion/)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

fake = Faker()
Faker.seed(42)
random.seed(42)


#  Connect to Postgres (details come from the .env file)

conn = psycopg2.connect(
    host=os.environ.get("POSTGRES_HOST", "localhost"),
    port=int(os.environ.get("POSTGRES_PORT", "5432")),
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
)
cur = conn.cursor()

# ------------------------------------------------------------
# 2. Empty the tables (they are created by ingestion/init.sql)
# ------------------------------------------------------------
cur.execute("""
truncate table raw.order_items, raw.orders, raw.products, raw.customers;
""")

# ------------------------------------------------------------
# 3. Generate fake data
# ------------------------------------------------------------
categories = ["Skincare", "Haircare", "Wellness", "Home"]
now = datetime.now()


def messy_email(email):
    # Real raw data is often untidy: mixed case or extra spaces.
    # Silver will clean this later.
    return random.choice([email, email.upper(), f"  {email}  "])


customers = [
    (
        i,
        fake.name(),
        messy_email(fake.email()),
        fake.city(),
        now - timedelta(days=random.randint(10, 30)),
    )
    for i in range(1, 11)
]   

products = [
    (
        i,
        f"{fake.word().title()} {random.choice(['Cream', 'Oil', 'Soap', 'Serum'])}",
        random.choice(categories),
        round(random.uniform(5, 100), 2),
    )
    for i in range(1, 6)
]
price_of = {p[0]: p[3] for p in products}

orders = []
order_items = []
item_id = 1
for order_id in range(1, 11):
    order_date = (now - timedelta(days=random.randint(0, 20))).date()
    orders.append((
        order_id,
        random.randint(1, 10),
        order_date,
        random.choice(["completed", "shipped", "cancelled"]),
        datetime.combine(order_date, datetime.min.time()),
    ))
    for _ in range(random.randint(1, 4)):
        product_id = random.randint(1, 5)
        order_items.append((
            item_id,
            order_id,
            product_id,
            random.randint(1, 5),
            price_of[product_id],
        ))
        item_id += 1

# ------------------------------------------------------------
# 4. Insert into Postgres
# ------------------------------------------------------------
cur.executemany(
    "insert into raw.customers (customer_id, full_name, email, city, created_at) "
    "values (%s, %s, %s, %s, %s)",
    customers,
)
cur.executemany(
    "insert into raw.products (product_id, product_name, category, price) "
    "values (%s, %s, %s, %s)",
    products,
)
cur.executemany(
    "insert into raw.orders (order_id, customer_id, order_date, status, updated_at) "
    "values (%s, %s, %s, %s, %s)",
    orders,
)
cur.executemany(
    "insert into raw.order_items (order_item_id, order_id, product_id, quantity, unit_price) "
    "values (%s, %s, %s, %s, %s)",
    order_items,
)

conn.commit()
cur.close()
conn.close()

print(
    f"Loaded {len(customers)} customers, {len(products)} products, "
    f"{len(orders)} orders, {len(order_items)} order items."
)