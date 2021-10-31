{{
    config(
        materialized='incremental',
        unique_key='date || table_name'
    )
}}

SELECT CURRENT_DATE AS date,
    relname AS table_name,
    n_live_tup AS row_count
FROM {{ source('pg_catalog', 'pg_stat_user_tables') }}
WHERE schemaname = 'public'
    AND (
        relname LIKE 'water_temp_%'
        OR relname LIKE 'table_stats'
    )
ORDER BY relname