# Quality vs. quantity of schooling - Data package

This data package contains the data that powers the chart ["Quality vs. quantity of schooling"](https://ourworldindata.org/grapher/quality-vs-quantity-of-schooling?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website.

## CSV Structure

The high level structure of the CSV file is that each row is an observation for an entity (usually a country or region) and a timepoint (usually a year).

The first two columns in the CSV file are "Entity" and "Code". "Entity" is the name of the entity (e.g. "United States"). "Code" is the OWID internal entity code that we use if the entity is a country or region. For normal countries, this is the same as the [iso alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) code of the entity (e.g. "USA") - for non-standard countries like historical countries these are custom codes.

The third column is either "Year" or "Day". If the data is annual, this is "Year" and contains only the year as an integer. If the column is "Day", the column contains a date string in the form "YYYY-MM-DD".

The remaining columns are the data columns, each of which is a time series. If the CSV data is downloaded using the "full data" option, then each column corresponds to one time series below. If the CSV data is downloaded using the "only selected data visible in the chart" option then the data columns are transformed depending on the chart type and thus the association with the time series might not be as straightforward.

## Metadata.json structure

The .metadata.json file contains metadata about the data package. The "charts" key contains information to recreate the chart, like the title, subtitle etc.. The "columns" key contains information about each of the columns in the csv, like the unit, timespan covered, citation for the data etc..

## About the data

Our World in Data is almost never the original producer of the data - almost all of the data we use has been compiled by others. If you want to re-use data, it is your responsibility to ensure that you adhere to the sources' license and to credit them correctly. Please note that a single time series may have more than one source - e.g. when we stich together data from different time periods by different producers or when we calculate per capita metrics using population data from a second source.

### How we process data at Our World In Data
All data and visualizations on Our World in Data rely on data sourced from one or several original data providers. Preparing this original data involves several processing steps. Depending on the data, this can include standardizing country names and world region definitions, converting units, calculating derived indicators such as per capita measures, as well as adding or adapting metadata such as the name or the description given to an indicator.
[Read about our data pipeline](https://docs.owid.io/projects/etl/)

## Detailed information about each time series


## Normalized  harmonized test scores among all students
The quality of schooling is assessed using the [harmonized learning scores](#dod:harmonized-scores), adjusted relative to the country with the highest performance, in this instance, Singapore.
Last updated: August 20, 2025  
Next update: August 2026  
Date range: 2010–2020  
Unit: index  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
World Bank (2024) – processed by Our World in Data

#### Full citation
World Bank (2024) – processed by Our World in Data. “Normalized  harmonized test scores among all students” [dataset]. World Bank, “Human Capital Index - Harmonized Test Scores” [original data].
Source: World Bank (2024) – processed by Our World In Data

### What you should know about this data
* Harmonized learning outcomes combine student test results into scores that can be compared across countries.
* This data includes developing countries that are often missing from major international tests by incorporating regional assessments.
* The data combines well-known international tests like [TIMSS, PIRLS](https://timssandpirls.bc.edu/), and [PISA](https://www.oecd.org/en/about/programmes/pisa.html) with regional tests like [SACMEQ](https://healtheducationresources.unesco.org/organizations/southern-and-eastern-africa-consortium-monitoring-educational-quality-sacmeq).
* Test scores are adjusted using statistical methods so they can be compared fairly across different subjects, grade levels, and testing years.
* This creates a dataset where countries can be compared on the same scale, accounting for differences in when tests were taken and what grades were tested.
* The scoring system is based on TIMSS standards where 300 points represents basic skills and 625 points shows advanced performance.
* Higher scores mean students in that country typically perform better on these academic tests, though the tests don't cover all subjects or age groups.

### Source

#### World Bank – Human Capital Index - Harmonized Test Scores
Retrieved on: 2025-08-20  
Retrieved from: https://www.worldbank.org/en/publication/human-capital  

#### Notes on our processing step for this indicator
Harmonized test scores are normalized to the country with the highest performance, in this case, Singapore. The normalization process involves dividing the country's score by the highest score.


## Expected years of schooling – UNDP
Number of years a child of school-entrance-age can expect to receive if the current age-specific enrollment rates persist throughout the child's life.
Last updated: May 7, 2025  
Next update: May 2026  
Date range: 1990–2023  
Unit: years  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
UNDP, Human Development Report (2025) – with minor processing by Our World in Data

#### Full citation
UNDP, Human Development Report (2025) – with minor processing by Our World in Data. “Expected years of schooling – UNDP” [dataset]. UNDP, Human Development Report, “Human Development Report” [original data].
Source: UNDP, Human Development Report (2025) – with minor processing by Our World In Data

### What you should know about this data
* This indicator shows how many years a student starting school in that year is expected to spend in education.  It's based on the enrollment patterns observed in that country in that specific year.
* The calculation looks at how many students are enrolled at each age and education level, then estimates how long a new student would stay in school if those patterns continued. This includes time spent repeating grades, not just the official length of each school level.
* It measures participation in schooling - how long students are likely to stay in school - rather than whether they actually learn or graduate.
* Higher numbers mean students spend more years in school, either because the official school system is longer or because many students repeat grades.
* UNDP originally obtained this indicator from: ICF Macro Demographic and Health Surveys (various years), UNESCO Institute for Statistics (2024) and United Nations Children's Fund (UNICEF) Multiple Indicator Cluster Surveys (various years).

### Source

#### UNDP, Human Development Report – Human Development Report
Retrieved on: 2025-05-07  
Retrieved from: https://hdr.undp.org/  


## Population
Population by country, available from 10,000 BCE to 2100, based on data and estimates from different sources.
Last updated: July 15, 2024  
Next update: July 2026  
Date range: 10000 BCE – 2100 CE  
Unit: people  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
HYDE (2023); Gapminder (2022); UN WPP (2024) – with major processing by Our World in Data

#### Full citation
HYDE (2023); Gapminder (2022); UN WPP (2024) – with major processing by Our World in Data. “Population” [dataset]. PBL Netherlands Environmental Assessment Agency, “History Database of the Global Environment 3.3”; Gapminder, “Population v7”; United Nations, “World Population Prospects”; Gapminder, “Systema Globalis” [original data].
Source: HYDE (2023); Gapminder (2022); UN WPP (2024) – with major processing by Our World In Data

### Sources

#### PBL Netherlands Environmental Assessment Agency – History Database of the Global Environment
Retrieved on: 2024-01-02  
Retrieved from: https://doi.org/10.24416/UU01-AEZZIT  

#### Gapminder – Population
Retrieved on: 2023-03-31  
Retrieved from: http://gapm.io/dpop  

#### United Nations – World Population Prospects
Retrieved on: 2024-07-11  
Retrieved from: https://population.un.org/wpp/downloads/  

#### Gapminder – Systema Globalis
Retrieved on: 2023-03-31  
Retrieved from: https://github.com/open-numbers/ddf--gapminder--systema_globalis  

#### Notes on our processing step for this indicator
### Combination of different sources
We construct our long-run population data by combining multiple sources:

- 10,000 BCE–1799: historical estimates by HYDE (v3.3).

- 1800–1949: historical estimates by Gapminder (v7).

- 1950–2023: population records from the United Nations World Population Prospects (2024 revision).

- 2024-2100: Projections based on Medium variant by the UN World Population Prospects (2024 revision).

**Geographical aggregates**

- For most years, we calculate aggregates by summing the population of member countries.
- We do this based on [our definition of continents](https://ourworldindata.org/world-region-map-definitions#our-world-in-data) and the [World Bank’s income groups](https://ourworldindata.org/grapher/world-bank-income-groups).
- The only exception is before 1800, where we use HYDE's estimates for continents (but not income groups).

For most of the years, we've estimated regional aggregates by summing the population of countries in each region. We've relied on [our continents](https://ourworldindata.org/world-region-map-definitions#our-world-in-data) and [World Bank income group definitions](https://ourworldindata.org/grapher/world-bank-income-groups). The only exception is before 1800, where we've used HYDE's estimates on continents (but not income groups).

**World**
- Before 1800: we use data from HYDE.
- 1800-1950: we estimate the global population by summing all available countries in the dataset.
- After 1950, we rely on estimates from the United Nations World Population Prospects.


## World regions according to WB
Regions as defined by the World Bank.
Last updated: January 1, 2023  
Date range: 2023–2023  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
World Bank – processed by Our World in Data

#### Full citation
World Bank – processed by Our World in Data. “World regions according to WB” [dataset]. World Bank, “World Bank Country and Lending Groups” [original data].
Source: World Bank – processed by Our World In Data

### Source

#### World Bank – World Bank Country and Lending Groups
Retrieved on: 2025-08-22  
Retrieved from: https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups  


    