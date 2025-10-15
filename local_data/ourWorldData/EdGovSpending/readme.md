# Education spending as share of total government spending - Data package

This data package contains the data that powers the chart ["Education spending as share of total government spending"](https://ourworldindata.org/grapher/share-of-education-in-government-expenditure?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website. It was downloaded on October 15, 2025.

### Active Filters

A filtered subset of the full data was downloaded. The following filters were applied:

## CSV Structure

The high level structure of the CSV file is that each row is an observation for an entity (usually a country or region) and a timepoint (usually a year).

The first two columns in the CSV file are "Entity" and "Code". "Entity" is the name of the entity (e.g. "United States"). "Code" is the OWID internal entity code that we use if the entity is a country or region. For normal countries, this is the same as the [iso alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) code of the entity (e.g. "USA") - for non-standard countries like historical countries these are custom codes.

The third column is either "Year" or "Day". If the data is annual, this is "Year" and contains only the year as an integer. If the column is "Day", the column contains a date string in the form "YYYY-MM-DD".

The final column is the data column, which is the time series that powers the chart. If the CSV data is downloaded using the "full data" option, then the column corresponds to the time series below. If the CSV data is downloaded using the "only selected data visible in the chart" option then the data column is transformed depending on the chart type and thus the association with the time series might not be as straightforward.

## Metadata.json structure

The .metadata.json file contains metadata about the data package. The "charts" key contains information to recreate the chart, like the title, subtitle etc.. The "columns" key contains information about each of the columns in the csv, like the unit, timespan covered, citation for the data etc..

## About the data

Our World in Data is almost never the original producer of the data - almost all of the data we use has been compiled by others. If you want to re-use data, it is your responsibility to ensure that you adhere to the sources' license and to credit them correctly. Please note that a single time series may have more than one source - e.g. when we stich together data from different time periods by different producers or when we calculate per capita metrics using population data from a second source.

## Detailed information about the data


## Government expenditure on education, total (% of government expenditure)
Last updated: September 8, 2025  
Next update: September 2026  
Date range: 1972–2023  
Unit: % of government expenditure  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
UIS.Stat Bulk Data Download Service (UNESCO UIS), via World Bank (2025) – processed by Our World in Data

#### Full citation
UIS.Stat Bulk Data Download Service (UNESCO UIS), via World Bank (2025) – processed by Our World in Data. “Government expenditure on education, total (% of government expenditure)” [dataset]. UIS.Stat Bulk Data Download Service (UNESCO UIS), via World Bank, “World Development Indicators 122” [original data].
Source: UIS.Stat Bulk Data Download Service (UNESCO UIS), via World Bank (2025) – processed by Our World In Data

### How is this data described by its producer - UIS.Stat Bulk Data Download Service (UNESCO UIS), via World Bank (2025)?
General government expenditure on education (current, capital, and transfers) is expressed as a percentage of total general government expenditure on all sectors (including health, education, social services, etc.). It includes expenditure funded by transfers from international sources to government. General government usually refers to local, regional and central governments.

### Limitations and exceptions:
Data on government expenditure on education may refer to spending by the ministry of education only (excluding spending on educational activities by other ministries). In addition, definitions and methods of data on total general government expenditure may differ across countries.

### Statistical concept and methodology:
Expenditure on education, total (% of government expenditure) is calculated by dividing total government expenditure on education by the total government expenditure on all sectors and multiplying by 100. Aggregate data are based on World Bank estimates.

Data on education are collected by the UNESCO Institute for Statistics from official responses to its annual education survey. All the data are mapped to the International Standard Classification of Education (ISCED) to ensure the comparability of education programs at the international level. The current version was formally adopted by UNESCO Member States in 2011. Data on total general government expenditure were previously collected from countries through the annual questionnaire, but are from the International Monetary Fund's World Economic Outlook database since January 2014. Therefore, current data cannot be compared with data in earlier editions.

The reference years reflect the school year for which the data are presented. In some countries the school year spans two calendar years (for example, from September 2010 to June 2011); in these cases the reference year refers to the year in which the school year ended (2011 in the example).

### Source

#### UIS.Stat Bulk Data Download Service (UNESCO UIS), via World Bank – World Development Indicators
Retrieved on: 2025-09-08  
Retrieved from: https://data.worldbank.org/indicator/SE.XPD.TOTL.GB.ZS  


    