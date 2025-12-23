# Completion rate of upper secondary education - Data package

This data package contains the data that powers the chart ["Completion rate of upper secondary education"](https://ourworldindata.org/grapher/completion-rate-of-upper-secondary-education-sdg?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website. It was downloaded on October 22, 2025.

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


## Completion rate in upper secondary education
The share of children who are three to five years older than the official age for the last grade of [upper secondary education](#dod:upper-secondary-education) education who have successfully completed it. This broader age band is used to include children who started school late or had to resit particular years.
Last updated: May 1, 2025  
Next update: May 2026  
Date range: 1990–2024  
Unit: %  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
UNESCO Institute for Statistics (2025) – with minor processing by Our World in Data

#### Full citation
UNESCO Institute for Statistics (2025) – with minor processing by Our World in Data. “Completion rate in upper secondary education” [dataset]. UNESCO Institute for Statistics, “UNESCO Institute for Statistics (UIS) - Education” [original data].
Source: UNESCO Institute for Statistics (2025) – with minor processing by Our World In Data

### What you should know about this data
* This indicator estimates the share of children who complete a given level of education, even if they do so later than the expected age.
* For example, if the official age of completion for primary school is 11 years old, a child who completes it at 14 years old would still be included. This is to account for the fact that some children may start school late, or have to repeat years.
* The data sources include household surveys, censuses, and administrative records, with modelled adjustments to improve comparability across countries.
* These estimates are produced using a statistical model that draws on these sources, filling gaps where direct observations are missing or inconsistent.
* Because values are estimated, they may differ from official national figures. Differences in school systems or grade structures can also affect comparability.

### Source

#### UNESCO Institute for Statistics – UNESCO Institute for Statistics (UIS) - Education
Retrieved on: 2025-05-01  
Retrieved from: https://databrowser.uis.unesco.org/resources/bulk  


    