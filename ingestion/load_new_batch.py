import os
import random
from datetime import datetime
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

conn = psycopg2.connect(
    host=os.environ.get("POSTGRES_HOST", "localhost"),
    port=int(os.environ.get("POSTGRES_PORT", "5432")),
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
)
cur = conn.cursor()

NEW_ORDERS = 5
STATUS_UPDATES = 4
now = datetime.now()

# Find the next free ids
cur.execute("""
    select
        (select coalesce(max(order_id), 0) from raw.orders),
        (select coalesce(max(order_item_id), 0) from raw.order_items)
""")
last_order_id, last_item_id = cur.fetchone()

cur.execute("select customer_id from raw.customers")
customer_ids = [row[0] for row in cur.fetchall()]

cur.execute("select product_id, price from raw.products")
price_of = dict(cur.fetchall())
product_ids = list(price_of)

# 1. New orders and their items
order_id, item_id = last_order_id, last_item_id
for _ in range(NEW_ORDERS):
    order_id += 1
    cur.execute(
        "insert into raw.orders (order_id, customer_id, order_date, status, updated_at) "
        "values (%s, %s, %s, %s, %s)",
        (order_id, random.choice(customer_ids), now.date(),
         random.choice(["completed", "shipped"]), now),
    )
    for _ in range(random.randint(1, 4)):
        item_id += 1
        product_id = random.choice(product_ids)
        cur.execute(
            "insert into raw.order_items "
            "(order_item_id, order_id, product_id, quantity, unit_price) "
            "values (%s, %s, %s, %s, %s)",
            (item_id, order_id, product_id, random.randint(1, 5), price_of[product_id]),
        )

# 2. Status changes on existing orders (shipped -> completed)
cur.execute("""
    update raw.orders
    set status = 'completed', updated_at = now(), loaded_at = now()
    where order_id in (
        select order_id from raw.orders
        where status = 'shipped' and order_id <= %s
        order by random() limit %s
    )
""", (last_order_id, STATUS_UPDATES))
updated = cur.rowcount

conn.commit()
cur.close()
conn.close()

print(f"Added {NEW_ORDERS} new orders ({item_id - last_item_id} items) "
      f"and updated {updated} existing orders.")