select
    api_user_id,
    name,
    username,
    email,
    phone,
    website
from {{ ref('stg_api_users') }}
