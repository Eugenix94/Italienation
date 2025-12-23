# GNI per capita vs. GDP per capita - Data package

This data package contains the data that powers the chart ["GNI per capita vs. GDP per capita"](https://ourworldindata.org/grapher/gni-per-capita-vs-gdp-per-capita?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website.

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


## Gross national income (GNI) per capita – In constant international-$ – World Bank
Average income per person earned by residents of a country or region, including income earned abroad. This data is adjusted for inflation and differences in living costs between countries.
Last updated: September 8, 2025  
Next update: September 2026  
Date range: 1990–2024  
Unit: international-$ in 2021 prices  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Eurostat, OECD, IMF, and World Bank (2025) – with minor processing by Our World in Data

#### Full citation
Eurostat, OECD, IMF, and World Bank (2025) – with minor processing by Our World in Data. “Gross national income (GNI) per capita – World Bank – In constant international-$” [dataset]. Eurostat, OECD, IMF, and World Bank, “World Development Indicators 122” [original data].
Source: Eurostat, OECD, IMF, and World Bank (2025) – with minor processing by Our World In Data

### What you should know about this data
* Gross national income (GNI) is a measure of the total income earned by residents of a country or region each year. It is calculated as GDP plus net income received from abroad, plus taxes (minus subsidies) on production. GNI per capita is GNI divided by population.
* This GNI per capita indicator provides information on economic growth and income levels from 1990.
* This data is adjusted for inflation and differences in living costs between countries.
* This data is expressed in [international-$](#dod:int_dollar_abbreviation) at 2021 prices.

### Source

#### Eurostat, OECD, IMF, and World Bank – World Development Indicators
Retrieved on: 2025-09-08  
Retrieved from: https://data.worldbank.org/indicator/NY.GNP.PCAP.PP.KD  


## GDP per capita – In constant international-$ – World Bank
Average economic output per person in a country or region per year. This data is adjusted for inflation and differences in living costs between countries.
Last updated: September 8, 2025  
Next update: September 2026  
Date range: 1990–2024  
Unit: international-$ in 2021 prices  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Eurostat, OECD, IMF, and World Bank (2025) – with minor processing by Our World in Data

#### Full citation
Eurostat, OECD, IMF, and World Bank (2025) – with minor processing by Our World in Data. “GDP per capita – World Bank – In constant international-$” [dataset]. Eurostat, OECD, IMF, and World Bank, “World Development Indicators 122” [original data].
Source: Eurostat, OECD, IMF, and World Bank (2025) – with minor processing by Our World In Data

### What you should know about this data
* GDP per capita is a comprehensive measure of people's average income. It helps compare income levels across countries and track how they change over time. It is especially useful for understanding trends in economic growth and living standards.
* GDP per capita is calculated as the value of all final goods and services produced each year in a country (the [gross domestic product](#dod:gdp)), divided by the population. It represents the average economic output per person.
* This indicator shows the large inequality between people in different countries. In the poorest countries, average incomes are below $1,000 per year; in rich countries, they are more than 50 times higher.
* This data is expressed in constant international dollars to adjust for inflation and differences in living costs between countries. Read more in our article, [What are international dollars?](https://ourworldindata.org/international-dollars)
* This data comes from the World Bank and starts in 1990. For estimates going back several centuries, explore our chart of GDP per capita from the [Maddison Project Database](https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database).

### Source

#### Eurostat, OECD, IMF, and World Bank – World Development Indicators
Retrieved on: 2025-09-08  
Retrieved from: https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD  


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


## World regions according to OWID
Regions defined by Our World in Data, which are used in OWID charts and maps.
Last updated: January 1, 2023  
Date range: 2023–2023  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Our World in Data – processed by Our World in Data

#### Full citation
Our World in Data – processed by Our World in Data. “World regions according to OWID” [dataset]. Our World in Data, “Regions” [original data].
Source: Our World in Data

### Source

#### Our World in Data – Regions


    