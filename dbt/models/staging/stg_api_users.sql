select
    cast(id as integer) as api_user_id,
    cast(name as text) as name,
    cast(username as text) as username,
    cast(email as text) as email,
    cast(phone as text) as phone,
    cast(website as text) as website
from {{ source('raw_zone', 'api_users') }}
where id is not null
