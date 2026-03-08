select
    cast(customer_id as integer) as customer_id,
    cast(customer_name as text) as customer_name,
    cast(country as text) as country
from {{ source('raw_zone', 'customers') }}
