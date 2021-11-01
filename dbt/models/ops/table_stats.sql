{{
    config(
        materialized='incremental',
        unique_key='date || table_name',
        pre_hook=[
            "{% set tables_to_analyze = [ref('water_temp_unique'), ref('water_temp_weekly_avg'), this] %}

            {%- for table in tables_to_analyze %}
                ANALYZE {{ table }};
            {% endfor %}"
        ]
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
