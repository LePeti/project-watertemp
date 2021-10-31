{{
    config(
        materialized='incremental',
        unique_key='date || relname'
    )
}}

SELECT 
    CURRENT_DATE AS date,
    relname,
    n_live_tup
FROM {{ source('pg_catalog', 'pg_stat_user_tables') }}
WHERE schemaname = 'public'
    AND (relname LIKE 'water_temp_%' OR relname LIKE 'table_stats')
ORDER BY relname