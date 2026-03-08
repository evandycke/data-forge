select
    orders.order_id,
    orders.customer_id,
    customers.customer_name,
    customers.country,
    orders.amount,
    orders.order_status,
    case
        when orders.amount >= 200 then 'large'
        when orders.amount >= 100 then 'medium'
        else 'small'
    end as order_size_bucket
from {{ ref('stg_orders') }} as orders
left join {{ ref('stg_customers') }} as customers
    on orders.customer_id = customers.customer_id
