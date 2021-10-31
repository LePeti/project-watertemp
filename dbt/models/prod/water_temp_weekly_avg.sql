{{
    config(
        materialized='incremental',
        unique_key='unique_key',
        post_hook=[
            "DELETE FROM {{ ref('water_temp_unique') }}
            WHERE (
                date_published::DATE < (
                    SELECT MAX(date_published::DATE) FROM {{ ref('water_temp_unique') }}
                ) - INTERVAL '1 MONTHS'
                AND name_of_water <> 'Magyar tavak'
            ) OR (
                date_published::DATE < (
                    SELECT MAX(date_published::DATE) FROM {{ ref('water_temp_unique') }}
                ) - INTERVAL '12 MONTHS'
                AND name_of_water = 'Magyar tavak'
            );"
        ]
    )
}}

SELECT
    location,
    name_of_water,
    DATE_TRUNC('week', date_published::TIMESTAMP)::DATE AS date_published_weekly,
    AVG(water_depth_cm::REAL) AS avg_water_depth_cm,
    AVG(water_temp_celsius::REAL) AS avg_water_temp_celsius,
    AVG(air_temp_celsius::REAL) AS avg_air_temp_celsius,
    location || '-' || name_of_water || '-' || DATE_TRUNC('week', date_published::TIMESTAMP)::DATE AS unique_key
FROM {{ ref('water_temp_unique') }}
{% if is_incremental() %}
    WHERE date_published::DATE >= (SELECT max(date_published_weekly) FROM {{ this }})
{% endif %}
GROUP BY 1, 2, 3
ORDER BY 3 DESC, 1, 2
