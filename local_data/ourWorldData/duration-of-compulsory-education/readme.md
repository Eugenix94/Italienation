# Duration of compulsory education - Data package

This data package contains the data that powers the chart ["Duration of compulsory education"](https://ourworldindata.org/grapher/duration-of-compulsory-education?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website. It was downloaded on October 22, 2025.

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


## Duration of compulsory education
The number of years of compulsory education is based on students starting at the earliest entrance age, studying full-time, and advancing without grade repetition or skipping.
Last updated: May 1, 2025  
Next update: May 2026  
Date range: 1975–2024  
Unit: years  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
UNESCO Institute for Statistics (2025) – with minor processing by Our World in Data

#### Full citation
UNESCO Institute for Statistics (2025) – with minor processing by Our World in Data. “Duration of compulsory education” [dataset]. UNESCO Institute for Statistics, “UNESCO Institute for Statistics (UIS) - Education” [original data].
Source: UNESCO Institute for Statistics (2025) – with minor processing by Our World In Data

### What you should know about this data
* The theoretical duration of compulsory education refers to the number of years that children are legally required to attend school, as defined by national laws or regulations.
* This indicator helps determine the school-age population by level of education and is a key input for producing education indicators and assessing a country's education supply capacity in relation to demand.
* The duration is typically calculated based on the official starting and ending ages for compulsory education, assuming students progress through the system without repeating or skipping grades.
* For example, if compulsory education starts at age 6 and ends at age 15, the theoretical duration would be 9 years.
* Data on compulsory education duration are collected from national legislation and formal education standards, and are mapped to the [International Standard Classification of Education (ISCED)](https://uis.unesco.org/en/topic/international-standard-classification-education-isced) to ensure international comparability.
* It's important to note that while legislation may define the duration of compulsory education, actual implementation and enforcement can vary, and some children may not attend school for the full duration.
* Changes in national education policies, such as extending or reducing the years of compulsory education, can impact this indicator and should be considered when analyzing trends over time.
* This indicator is useful for understanding government commitment to education and for planning resource allocation, but it should be interpreted alongside other indicators like enrolment rates and completion rates for a comprehensive view.
* Limitations include potential discrepancies between legal provisions and actual practice, and differences in how countries define and implement compulsory education.

### How is this data described by its producer - UNESCO Institute for Statistics (2025)?
Number of years that children are legally obliged to attend school.

### Source

#### UNESCO Institute for Statistics – UNESCO Institute for Statistics (UIS) - Education
Retrieved on: 2025-05-01  
Retrieved from: https://databrowser.uis.unesco.org/resources/bulk  


    