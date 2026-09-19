# World-Development-Analysis-SQL-Python

# Overview
An end-to-end Data Analyst portfolio project using Human Development Index (HDI) and World Bank indicators. It covers data cleaning, SQL analysis, Python EDA, correlation analysis, and visualization.

## Analytical Questions
- How are countries distributed across HDI categories?
- Which countries had the highest/lowest HDI in 2021?
- How does HDI vary by region?
- How did HDI change from 1990 to 2021?
- What is the relationship between HDI and GDP per capita?
- What is the relationship between HDI and Internet usage?
- What data-quality issues exist?

## Source Data
**HDI.csv:** country-level HDI and development indicators, with historical values from 1990–2021.
**WorldBank.xlsx:** socioeconomic indicators from 1960–2018, including GDP, GDP per capita, Internet usage, mortality, population density and unemployment.
**world_indicators_data_dictionary.csv:** definitions of World Bank fields.

## Tech Stack
- Python
- Pandas
- NumPy
- Matplotlib
- SQLite
- Excel
  
## SQL Analysis
The SQL script demonstrates SELECT, filtering, aggregation, GROUP BY, ORDER BY, JOINs, ranking and time-period comparisons.
Example:
```sql
SELECT region,
       COUNT(*) AS countries,
       ROUND(AVG(hdi_2021),3) AS avg_hdi_2021
FROM hdi_2021
WHERE region IS NOT NULL
GROUP BY region
ORDER BY avg_hdi_2021 DESC;

**## Python Workflow

```text
Load → Clean → Validate → EDA → Transform → Join → Correlation → Visualize → Export
```

The Python script creates seven PNG visualizations and exports analytical result tables.

## Key Findings
- The HDI file contains 206 country/territory records.
- 2021 HDI categories include Very High, High, Medium and Low; some records have missing categories.
- Regional averages differ substantially in the supplied data.
- HDI 2021 has a positive association with GDP per capita and Internet usage in the matched 2018 World Bank records.
- The analysis treats these relationships as associations, not causal effects.

## Important Time-Period Note
The World Bank source supplied with this project ends in **2018**, while the HDI source extends to **2021**. Therefore, the cross-dataset scatter plots compare **HDI 2021** with **World Bank 2018** indicators. This is not a same-year comparison and is explicitly documented to avoid misleading interpretation.

## Data Quality
The files contain missing values, especially for some historical HDI indicators and some World Bank measures. The analysis uses explicit null handling and only uses available observations for each calculation.

## Visualizations
1. HDI distribution — 2021
2. Top 10 HDI countries
3. Bottom 10 HDI countries
4. Average HDI by region
5. HDI trend, 1990–2021
6. HDI vs GDP per capita
7. HDI vs Internet usage

## Conclusion

This project demonstrates an end-to-end analytical workflow using real-world development indicators.
The analysis shows how HDI can be explored together with economic and digital indicators to understand differences between countries and regions.
The project intentionally separates:
- descriptive findings from
- statistical associations and
- causal claims
because correlation between indicators does not establish causation.


