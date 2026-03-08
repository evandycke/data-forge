select
    cast(order_id as integer) as order_id,
    cast(customer_id as integer) as customer_id,
    cast(amount as numeric(12, 2)) as amount,
    cast(status as text) as order_status
from {{ source('raw_zone', 'orders') }}
