# Literacy rate vs. average years of schooling - Data package

This data package contains the data that powers the chart ["Literacy rate vs. average years of schooling"](https://ourworldindata.org/grapher/literacy-rates-vs-average-years-of-schooling?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website.

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


## Literacy rate
Share of adults who can read and write a simple statement about their everyday life.
Last updated: June 11, 2025  
Next update: June 2026  
Date range: 1475–2023  
Unit: %  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
UNESCO (1957) and other sources – with major processing by Our World in Data

#### Full citation
UNESCO (1957); UNESCO (1953); Buringh and van Zanden (2009); van Zanden, J. et al.; UNESCO Institute for Statistics (2025) – with major processing by Our World in Data. “Literacy rate” [dataset]. UNESCO, “World illiteracy at mid-century”; UNESCO, “Progress of literacy in various countries”; Buringh and van Zanden, “Charting the “Rise of the West”: Manuscripts and Printed Books in Europe, A Long-Term Perspective from the Sixth through Eighteenth Centuries”; van Zanden, J. et al., “How Was Life? Global Well-being since 1820 - Education 2014”; UNESCO Institute for Statistics, “UNESCO Institute for Statistics (UIS) - Education” [original data].
Source: UNESCO (1957), UNESCO (1953), Buringh and van Zanden (2009), van Zanden, J. et al., UNESCO Institute for Statistics (2025) – with major processing by Our World In Data

### What you should know about this data
* Literacy is a foundational skill. Children need to learn to read so that they can read to learn. When we fail to teach this foundational skill, people have fewer opportunities to lead the rich and interesting lives that a good education offers. This indicator measures the percentage of people aged 15 and older who can read and write a simple sentence about their daily life.
* Historical data shows that only a very small share of the population, a tiny elite, was able to read and write. Although literacy has increased over the last few generations, it remains an important challenge for our time to [provide this foundational skill to all](https://ourworldindata.org/better-learning).
* However, measuring literacy over time is difficult, as definitions of what it means to be “literate” have varied widely across countries and historical periods. As a result, comparisons should be made with caution.
* Our team investigated the strengths and shortcomings of the available data on literacy. Based on this work, we've combined historical and contemporary literacy rates from various sources to provide a long-term view of global literacy trends from 1451 to the present. For detailed information on where each data point comes from, you can view and download this [Google Sheet](https://docs.google.com/spreadsheets/d/16Q4CD8ktFhdKUaIb4ab7angUmTachnIKtLR4nKz4UEI/edit).
* Many developed countries have discontinued literacy tracking as rates approached universal levels by the late 20th century, making measurement less relevant for policy purposes.
* All of this data measures basic literacy — can you read simple text and write your name? It doesn't capture *functional* literacy — can you understand a job application or follow written instructions? That requires years more education and is much harder to measure historically.

### How is this data described by its producer - UNESCO (1957), UNESCO (1953), Buringh and van Zanden (2009), van Zanden, J. et al., UNESCO Institute for Statistics (2025)?
The current UNESCO standard for defining literacy is the percentage of the population aged 15 and above who can read, understand, and write a short, simple statement on their everyday life. Generally, “literacy” also encompasses “numeracy”, the ability to make simple arithmetic calculations.

### Sources

#### UNESCO – World illiteracy at mid-century
Retrieved on: 2025-06-10  
Retrieved from: https://unesdoc.unesco.org/ark:/48223/pf0000002930  

#### UNESCO – Progress of literacy in various countries
Retrieved on: 2025-06-10  
Retrieved from: https://unesdoc.unesco.org/ark:/48223/pf0000002898  

#### Buringh and van Zanden – Charting the “Rise of the West”: Manuscripts and Printed Books in Europe, A Long-Term Perspective from the Sixth through Eighteenth Centuries
Retrieved on: 2025-06-09  
Retrieved from: https://www.researchgate.net/publication/46544350_Charting_the_Rise_of_the_West_Manuscripts_and_Printed_Books_in_Europe_A_Long-Term_Perspective_from_the_Sixth_through_Eighteenth_Centuries  

#### van Zanden, J. et al. – How Was Life? Global Well-being since 1820 - Education
Retrieved on: 2023-08-14  
Retrieved from: https://www.oecd-ilibrary.org/economics/how-was-life/education-since-1820_9789264214262-9-en  

#### UNESCO Institute for Statistics – UNESCO Institute for Statistics (UIS) - Education
Retrieved on: 2025-05-01  
Retrieved from: https://databrowser.uis.unesco.org/resources/bulk  

#### Notes on our processing step for this indicator
- This dataset combines historical and contemporary literacy rates from various sources to provide a long-term view of global literacy trends from 1451 to the present.
- 1451–1800: Direct literacy surveys did not exist during this period. Data for Great Britain, Ireland, France, Belgium, the Netherlands, Germany, Italy, Spain, Sweden, and Poland comes from the "[Charting the Rise of the West](https://www.researchgate.net/publication/46544350_Charting_the_Rise_of_the_West_Manuscripts_and_Printed_Books_in_Europe_A_Long-Term_Perspective_from_the_Sixth_through_Eighteenth_Centuries)" study. The authors estimated literacy rates using manuscript and book production as indirect indicators. While more books likely indicated more readers, this approach has clear limitations.
- 1820–1970 (Global estimates): Estimates for worldwide literacy are drawn from the OECD's “[How Was Life? Global Wellbeing Since 1820](https://www.oecd.org/en/publications/how-was-life_9789264214262-en.html)” report, which compiled a global long-run estimate of literacy using available historical records. A key limitation is that early literacy measures often accepted minimal skills — such as the ability to sign marriage documents — which fall short of contemporary literacy standards involving actual reading and writing proficiency.
- 1900–1950: UNESCO's “[Progress of literacy in various countries](https://unesdoc.unesco.org/ark:/48223/pf0000002898)” gathered data from 26 countries, revealing substantial variation in definitions. Some countries required only reading or writing skills, others demanded both, and some accepted signature ability as sufficient proof. Age thresholds also varied widely, ranging from 5 to 15 years.
- 1950: UNESCO's “[World Illiteracy at Mid-Century](https://unesdoc.unesco.org/ark:/48223/pf0000002930)” marked a significant milestone as the first comprehensive global literacy assessment. Data primarily came from censuses conducted between 1945 and 1954 for populations aged 15 and older. Where census data was unavailable, researchers generated estimates using historical trends and country-specific factors. Given the uncertainty, literacy rates were reported in 5% intervals. This data is reported as a range (e.g., 10–20%). These ranges were converted into single-point estimates by taking their midpoint to allow for consistent analysis. For example, 10–20% was recoded as 15%.
- 1970–present: Contemporary data comes from the [UNESCO Institute for Statistics](https://databrowser.uis.unesco.org/resources/bulk), based on population censuses or household surveys, and is often self-reported. A person is considered literate if they can read and write a short, simple sentence about everyday life. Many countries also include basic numeracy in this definition. Rates are shown as the percentage of the population aged 15 and above who meet this threshold.
- When only the illiteracy rate was reported, the literacy rate was calculated by subtracting it from 100%.


## Average years of education for 15-64 years olds
Average years of formal education for individuals aged 15-64.
Last updated: July 17, 2023  
Date range: 1870–2040  
Unit: years  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Barro and Lee (2015); Lee and Lee (2016) – with major processing by Our World in Data

#### Full citation
Barro and Lee (2015); Lee and Lee (2016) – with major processing by Our World in Data. “Average years of education for 15-64 years olds” [dataset]. Barro and Lee, “Projections of Educational Attainment”; Lee and Lee, “Human Capital in the Long Run” [original data].
Source: Barro and Lee (2015), Lee and Lee (2016) – with major processing by Our World In Data

### What you should know about this data
* For the years leading up to 2015, the data are derived from historical estimates, providing a retrospective view of education levels. For the years 2015 and beyond, the projections are grounded in the historical data of 2010, which serve as the foundational benchmark. These forward-looking projections are then crafted by analyzing trends in school enrollment and changes in population structures. These trends are informed by forecasts from the United Nations, ensuring a global perspective and understanding of future educational developments.
* The method to estimate average years of schooling takes into account the age distribution in the population. This is important because access to education can vary significantly across generations. Older generations may have had fewer educational opportunities than younger ones, which affects the overall average education level.
* It also considers the typical duration required to complete each education level. For instance, primary education usually takes about 6 years, secondary education 4-6 years, and higher education may take even longer. Understanding the time investment required for different education levels is essential for accurate assessment.
* At its core, the method calculates the average years of schooling. This is achieved by determining the percentage of the population that has completed each education level and multiplying it by the duration of that level. The sum of these results gives a comprehensive view of both the extent of educational attainment and the time spent in education by the population.
* The method is dynamic, adapting to changes over time and across regions. For example, if a country increases the length of primary education, this change is included in subsequent calculations. This adaptability ensures that the average years of education remain relevant and accurate over time and across different educational systems.
* Note that the method does not take into account the quality of education. It only considers the number of years spent in education. This means that the average years of schooling may not reflect the actual skills and knowledge of the population.

### Sources

#### Barro and Lee – Projections of Educational Attainment
Retrieved on: 2023-11-20  
Retrieved from: http://www.barrolee.com/  

#### Lee and Lee – Human Capital in the Long Run
Retrieved on: 2023-11-20  
Retrieved from: https://barrolee.github.io/BarroLeeDataSet/DataLeeLee.html  

#### Notes on our processing step for this indicator
Historical data up to the year 2010 has been sourced from 'Human Capital in the Long Run' by Lee and Lee (2016). This historical data was then combined with recent projections provided by Barro ane Lee (2015).

Regional aggregates were computed by Our World in Data through yearly population-weighted averages, where annual values are proportionally adjusted to emphasize the influence of larger populations.



## Population
Population by country, available from 10,000 BCE to 2023, based on data and estimates from different sources.
Last updated: July 15, 2024  
Next update: July 2026  
Date range: 10000 BCE – 2023 CE  
Unit: people  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
HYDE (2023); Gapminder (2022); UN WPP (2024) – with major processing by Our World in Data

#### Full citation
HYDE (2023); Gapminder (2022); UN WPP (2024) – with major processing by Our World in Data. “Population – HYDE, Gapminder, UN – Long-run data” [dataset]. PBL Netherlands Environmental Assessment Agency, “History Database of the Global Environment 3.3”; Gapminder, “Population v7”; United Nations, “World Population Prospects”; Gapminder, “Systema Globalis” [original data].
Source: HYDE (2023); Gapminder (2022); UN WPP (2024) – with major processing by Our World In Data

### What you should know about this data
* Population is the most commonly used metric throughout Our World in Data. It is used directly to understand population growth over time, and indirectly to calculate per-capita indicators, making it easier to compare countries of different sizes.
* We construct this indicator by combining multiple sources covering different periods.
  - HYDE v3.3 (2023): historical estimates from 10,000 BCE to 1799.
  - Gapminder v7 (2022): for 1800-1949.
  - UN World Population Prospects (2024): for 1950 onwards, including 2100 projections.
  - Gapminder Systema Globalis (2023): additional source for former countries (Yugoslavia, USSR, etc.)
* Breaks in the data may occur at the boundaries between sources due to their methodological differences.
* You can read more about the sources and methodology in our [dedicated article](https://ourworldindata.org/population-sources). We also provide a table of sources showing the source we use for each country-year.
* We calculate geographical aggregates (continents, income groups, etc.) by summing individual country populations. For years before 1800, we rely directly on HYDE's values for continents to ensure historical consistency.

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


    