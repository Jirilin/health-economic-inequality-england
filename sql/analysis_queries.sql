
-- HEALTH & ECONOMIC INEQUALITY ANALYSIS


-- 1. Top 10 most deprived areas
SELECT
    area_name,
    imd_average_score_rank,
    imd_deprivation_percentile,
    imd_most_deprived_10pct_share
FROM analytics_snapshot
ORDER BY imd_deprivation_percentile DESC
LIMIT 10;


-- 2. Lowest healthy life expectancy
SELECT
    area_name,
    healthy_life_expectancy_sex_mean,
    economic_inactivity_pct
FROM analytics_snapshot
WHERE healthy_life_expectancy_sex_mean IS NOT NULL
ORDER BY healthy_life_expectancy_sex_mean ASC
LIMIT 10;


-- 3. Highest economic inactivity
SELECT
    area_name,
    economic_inactivity_pct,
    healthy_life_expectancy_sex_mean
FROM analytics_snapshot
WHERE economic_inactivity_pct IS NOT NULL
ORDER BY economic_inactivity_pct DESC
LIMIT 10;


-- 4. Areas with poor health AND high inactivity
SELECT
    area_name,
    healthy_life_expectancy_sex_mean,
    economic_inactivity_pct,
    imd_deprivation_percentile
FROM analytics_snapshot
WHERE
    healthy_life_expectancy_sex_mean <
    (
        SELECT AVG(
            healthy_life_expectancy_sex_mean
        )
        FROM analytics_snapshot
    )
AND
    economic_inactivity_pct >
    (
        SELECT AVG(economic_inactivity_pct)
        FROM analytics_snapshot
    )
ORDER BY
    imd_deprivation_percentile DESC;


-- 5. Estimated years outside good health
SELECT
    area_name,
    life_expectancy_sex_mean,
    healthy_life_expectancy_sex_mean,
    unhealthy_years_estimate
FROM analytics_snapshot
WHERE unhealthy_years_estimate IS NOT NULL
ORDER BY unhealthy_years_estimate DESC
LIMIT 15;