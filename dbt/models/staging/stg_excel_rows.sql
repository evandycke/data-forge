select
    cast(customer_id as integer) as customer_id,
    cast(customer_name as text) as customer_name,
    cast(country as text) as country,
    cast(_sheet_name as text) as sheet_name
from {{ source('raw_zone', 'excel_rows') }}
