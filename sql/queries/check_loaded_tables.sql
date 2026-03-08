SELECT
    n.nspname AS schema_name,
    c.relname AS table_name
FROM pg_catalog.pg_class AS c
INNER JOIN pg_catalog.pg_namespace AS n
    ON n.oid = c.relnamespace
WHERE c.relkind = 'r'
  AND n.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY n.nspname, c.relname;
