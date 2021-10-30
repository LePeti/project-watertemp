-- Testing if NULL values in the unique table don't NULL out the weekly averages
-- Takeaway as of 2021-10-30: no they don't
WITH avg_nulls AS (
    SELECT location,
        name_of_water,
        date_published_weekly
    FROM water_temp_weekly_avg
    WHERE avg_water_depth_cm IS NOT NULL
),
uniqued AS (
    SELECT location,
        name_of_water,
        date_published,
        water_depth_cm,
        DATE_TRUNC('week', date_published::TIMESTAMP)::DATE AS date_published_weekly
    FROM water_temp_unique
)
SELECT *
FROM uniqued
    JOIN avg_nulls USING(location, name_of_water, date_published_weekly)
WHERE water_depth_cm IS NULL

-- An example: The below returns a few rows with NULL water_depth_cm but the weekly averages calculate normally and disregard nulls
    -- SELECT location,
    --     name_of_water,
    --     date_published,
    --     water_depth_cm,
    --     date_published
    -- FROM water_temp_unique
    -- WHERE location = 'Fertő'
    -- ORDER BY 3 DESC
