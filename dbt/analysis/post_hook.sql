SELECT *
FROM {{ ref('water_temp_unique') }}
WHERE (
        date_published::DATE < (
            SELECT MAX(date_published::DATE)
            FROM {{ ref('water_temp_unique') }}
        ) - INTERVAL '1 MONTHS'
        AND name_of_water <> 'Magyar tavak'
    )
    OR (
        date_published::DATE < (
            SELECT MAX(date_published::DATE)
            FROM {{ ref('water_temp_unique') }}
        ) - INTERVAL '12 MONTHS'
        AND name_of_water = 'Magyar tavak'
    )