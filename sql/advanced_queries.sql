
-- HEIVA ADVANCED ANALYSIS


-- 1. Highest vulnerability areas
SELECT
    area_name,
    vulnerability_score,
    segment_name
FROM analytics_enriched
ORDER BY vulnerability_score DESC
LIMIT 20;


-- 2. Cluster sizes
SELECT
    segment_name,
    COUNT(*) AS number_of_areas,
    AVG(vulnerability_score)
        AS average_heiva_score
FROM analytics_enriched
GROUP BY segment_name
ORDER BY average_heiva_score DESC;


-- 3. Latest health trends
SELECT
    area_name,
    first_value,
    latest_value,
    absolute_change,
    percentage_change
FROM area_trends
WHERE indicator =
    'healthy_life_expectancy'
ORDER BY absolute_change ASC;


-- 4. Areas where economic inactivity increased
SELECT
    area_name,
    first_period,
    latest_period,
    first_value,
    latest_value,
    absolute_change
FROM area_trends
WHERE
    indicator =
        'economic_inactivity'
AND
    absolute_change > 0
ORDER BY
    absolute_change DESC;


-- 5. High vulnerability + increasing inactivity
SELECT
    a.area_name,
    a.vulnerability_score,
    a.segment_name,
    t.absolute_change
        AS inactivity_change
FROM analytics_enriched AS a
JOIN area_trends AS t
    ON a.area_code =
       t.area_code
WHERE
    t.indicator =
        'economic_inactivity'
AND
    t.absolute_change > 0
AND
    a.vulnerability_score >= 75
ORDER BY
    a.vulnerability_score DESC;


-- 6. Future illustrative projections
SELECT
    area_name,
    forecast_year,
    predicted_economic_inactivity,
    historical_r_squared
FROM economic_inactivity_forecast
ORDER BY
    predicted_economic_inactivity DESC;