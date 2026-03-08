select
    'api_users' as dataset_name,
    count(*) as row_count
from {{ ref('stg_api_users') }}

union all

select
    'txt_lines' as dataset_name,
    count(*) as row_count
from {{ ref('stg_txt_lines') }}

union all

select
    'excel_rows' as dataset_name,
    count(*) as row_count
from {{ ref('stg_excel_rows') }}

union all

select
    'customers' as dataset_name,
    count(*) as row_count
from {{ ref('stg_customers') }}

union all

select
    'orders' as dataset_name,
    count(*) as row_count
from {{ ref('stg_orders') }}
