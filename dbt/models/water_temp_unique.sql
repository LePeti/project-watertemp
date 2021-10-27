{{
    config(
        materialized='incremental',
        post_hook=[
          "DELETE FROM {{ source('public', 'water_temp_raw') }}
           WHERE date_published::DATE < (
             SELECT MAX(date_published::DATE) FROM {{ source('public', 'water_temp_raw') }}
           ) - INTERVAL '2 MONTH';"
        ]
    )
}}

SELECT
  location,
  water_depth_cm,
  water_temp_celsius,
  air_temp_celsius,
  name_of_water,
  MAX(time_of_scraping_cet) AS time_of_scraping_cet,
  date_published
FROM {{ source('public', 'water_temp_raw') }}
{% if is_incremental() %}
  WHERE date_published > (SELECT max(date_published) FROM {{ this }})
{% endif %}
GROUP BY location,
  water_depth_cm,
  water_temp_celsius,
  air_temp_celsius,
  name_of_water,
  date_published
