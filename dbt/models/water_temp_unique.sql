{{
    config(
        materialized='incremental'
    )
}}

SELECT DISTINCT *
FROM {{ source('public', 'water_temp_raw') }}
{% if is_incremental() %}
  WHERE date_published > (SELECT max(date_published) FROM {{ this }})
{% endif %}
