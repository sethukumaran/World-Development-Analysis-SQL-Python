-- WORLD DEVELOPMENT SQL ANALYSIS

-- 1. HDI country coverage
SELECT COUNT(*) AS countries, COUNT(DISTINCT iso3) AS unique_country_codes
FROM hdi_2021;

-- 2. HDI category distribution
SELECT hdicode, COUNT(*) AS country_count
FROM hdi_2021
WHERE hdicode IS NOT NULL
GROUP BY hdicode
ORDER BY country_count DESC;

-- 3. Top 10 HDI countries in 2021
SELECT country, region, hdi_2021, hdi_rank_2021
FROM hdi_2021
WHERE hdi_rank_2021 IS NOT NULL
ORDER BY hdi_rank_2021
LIMIT 10;

-- 4. Bottom 10 HDI countries in 2021
SELECT country, region, hdi_2021, hdi_rank_2021
FROM hdi_2021
WHERE hdi_rank_2021 IS NOT NULL
ORDER BY hdi_rank_2021 DESC
LIMIT 10;

-- 5. Average HDI by region
SELECT region, COUNT(*) AS countries, ROUND(AVG(hdi_2021),3) AS avg_hdi_2021
FROM hdi_2021
WHERE region IS NOT NULL
GROUP BY region
ORDER BY avg_hdi_2021 DESC;

-- 6. HDI improvement from 1990 to 2021
SELECT h.country,h.region,t90.hdi AS hdi_1990,t21.hdi AS hdi_2021,
       ROUND(t21.hdi-t90.hdi,3) AS hdi_change
FROM hdi_2021 h
JOIN hdi_timeseries t90 ON h.iso3=t90.iso3 AND t90.year=1990
JOIN hdi_timeseries t21 ON h.iso3=t21.iso3 AND t21.year=2021
WHERE t90.hdi IS NOT NULL AND t21.hdi IS NOT NULL
ORDER BY hdi_change DESC
LIMIT 20;

-- 7. World Bank latest available year: 2018
SELECT country_name,region,income_group,gdp_per_capita_usd,internet_pct,unemployment_pct
FROM worldbank
WHERE year=2018
ORDER BY gdp_per_capita_usd DESC
LIMIT 20;

-- 8. Regional World Bank summary for 2018
SELECT region,COUNT(*) AS countries,
       ROUND(AVG(gdp_per_capita_usd),2) AS avg_gdp_per_capita,
       ROUND(AVG(internet_pct),2) AS avg_internet_pct
FROM worldbank
WHERE year=2018
GROUP BY region
ORDER BY avg_gdp_per_capita DESC;

-- 9. HDI + World Bank join
SELECT h.country,h.region,h.hdi_2021,w.gdp_per_capita_usd,w.internet_pct,w.unemployment_pct
FROM hdi_2021 h
JOIN worldbank w ON h.iso3=w.country_code
WHERE w.year=2018
ORDER BY h.hdi_2021 DESC;

-- 10. High-HDI countries with lower Internet usage
SELECT h.country,h.hdi_2021,w.internet_pct,w.gdp_per_capita_usd
FROM hdi_2021 h
JOIN worldbank w ON h.iso3=w.country_code
WHERE w.year=2018 AND h.hdi_2021>=0.80
  AND w.internet_pct IS NOT NULL AND w.internet_pct<70
ORDER BY h.hdi_2021 DESC;

-- 11. Correlation-ready dataset for Python
SELECT h.country,h.region,h.hdi_2021,w.gdp_per_capita_usd,w.internet_pct,
       w.population_density,w.unemployment_pct
FROM hdi_2021 h
JOIN worldbank w ON h.iso3=w.country_code
WHERE w.year=2018 AND h.hdi_2021 IS NOT NULL;
