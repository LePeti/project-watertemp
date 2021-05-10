SELECT DISTINCT *
FROM {{ source('public', 'water_temp_raw') }}
