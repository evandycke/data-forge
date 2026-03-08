select
    cast(line_number as integer) as line_number,
    cast(text as text) as line_text,
    cast(file_name as text) as file_name
from {{ source('raw_zone', 'txt_lines') }}
