create schema if not exists raw;

create table if not exists raw.customers (
    customer_id int primary key,
    full_name   text,
    email       text,
    city        text,
    created_at  timestamp,
    loaded_at   timestamp default now()
);

create table if not exists raw.products (
    product_id   int primary key,
    product_name text,
    category     text,
    price        numeric(10,2),
    loaded_at    timestamp default now()
);

create table if not exists raw.orders (
    order_id    int primary key,
    customer_id int,
    order_date  date,
    status      text,
    updated_at  timestamp,
    loaded_at   timestamp default now()
);

create table if not exists raw.order_items (
    order_item_id int primary key,
    order_id      int,
    product_id    int,
    quantity      int,
    unit_price    numeric(10,2),
    loaded_at     timestamp default now()
);
