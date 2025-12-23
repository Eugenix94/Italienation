# Share of employment in agriculture, industry, and services - Data package

This data package contains the data that powers the chart ["Share of employment in agriculture, industry, and services"](https://ourworldindata.org/grapher/share-employment-agriculture-industry-services?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website.

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


## Agriculture
Share of total employment working in the agriculture sector.
Last updated: September 8, 2025  
Next update: September 2026  
Date range: 1991–2023  
Unit: %  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank (2025) – processed by Our World in Data

#### Full citation
ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank (2025) – processed by Our World in Data. “Agriculture – ILO” [dataset]. ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank, “World Development Indicators 122” [original data].
Source: ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank (2025) – processed by Our World In Data

### What you should know about this data
* Employment refers to all persons of working age who, during a specified brief period, were in paid employment or self-employment.
* The agriculture sector includes crop and animal production, hunting, forestry, logging, and fishing and aquaculture activities, as defined by the [International Standard Industrial Classification of All Economic Activities (ISIC)](https://ilostat.ilo.org/methods/concepts-and-definitions/classification-economic-activities/) (category A in ISIC revision 4).
* This data is part of the ILO Modelled Estimates series. This series combines nationally reported observations with imputed data to have a harmonized, internationally comparable dataset and produce regional and global aggregates. For more information, please refer to the [ILO Modelled Estimates documentation](https://ilostat.ilo.org/methods/concepts-and-definitions/ilo-modelled-estimates/).
* This data is classified according to the 13th International Classification of Labour Statistics (ICLS), where employment includes anyone engaged for at least one hour per day in the production of goods and services, even for own use by the household or family, volunteering, or other forms of unpaid work. For more information, please refer to [this explainer by the International Labour Organization](https://www.ilo.org/publications/quick-guide-understanding-impact-new-statistical-standards-ilostat).

### How is this data described by its producer - ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank (2025)?
Employment is defined as persons of working age who were engaged in any activity to produce goods or provide services for pay or profit, whether at work during the reference period or not at work due to temporary absence from a job, or to working-time arrangement. The agriculture sector consists of activities in agriculture, hunting, forestry and fishing, in accordance with division 1 (ISIC 2) or categories A-B (ISIC 3) or category A (ISIC 4).

### Limitations and exceptions:
There are many differences in how countries define and measure employment status, particularly members of the armed forces, self-employed workers, and unpaid family workers. Where members of the armed forces are included, they are allocated to the service sector, causing that sector to be somewhat overstated relative to the service sector in economies where they are excluded. Where data are obtained from establishment surveys, data cover only employees; thus self-employed and unpaid family workers are excluded. In such cases the employment share of the agricultural sector is severely underreported. Caution should be also used where the data refer only to urban areas, which record little or no agricultural work. Moreover, the age group and area covered could differ by country or change over time within a country. For detailed information, consult the original source.

Countries also take different approaches to the treatment of unemployed people. In most countries unemployed people with previous job experience are classified according to their last job. But in some countries the unemployed and people seeking their first job are not classifiable by economic activity. Because of these differences, the size and distribution of employment by economic activity may not be fully comparable across countries.

The ILO reports data by major divisions of the ISIC revision 2, revision 3, or revision 4. Broad classification such as employment by agriculture, industry, and services may obscure fundamental shifts within countries' industrial patterns. A slight majority of countries report economic activity according to the ISIC revision 3 instead of revision 2 or revision 4. The use of one classification or the other should not have a significant impact on the information for the employment of the three broad sectorsdata.

### Statistical concept and methodology:
The International Labour Organization (ILO) classifies economic activity using the International Standard Industrial Classification (ISIC) of All Economic Activities, revision 2 (1968), revision 3 (1990), and revision 4 (2008). Because this classification is based on where work is performed (industry) rather than type of work performed (occupation), all of an enterprise's employees are classified under the same industry, regardless of their trade or occupation. The categories should sum to 100 percent. Where they do not, the differences are due to workers who are not classified by economic activity.

The series is part of the "ILO modeled estimates database," including nationally reported observations and imputed data for countries with missing data, primarily to capture regional and global trends with consistent country coverage. Country-reported microdata is based mainly on nationally representative labor force surveys, with other sources (e.g., household surveys and population censuses) considering differences in the data source, the scope of coverage, methodology, and other country-specific factors. Country analysis requires caution where limited nationally reported data are available. A series of models are also applied to impute missing observations and make projections. However, imputed observations are not based on national data, are subject to high uncertainty, and should not be used for country comparisons or rankings. For more information: https://ilostat.ilo.org/resources/concepts-and-definitions/ilo-modelled-estimates/

### Notes from original source:
Given the exceptional situation, including the scarcity of relevant data, the ILO modeled estimates and projections from 2020 onwards are subject to substantial uncertainty.

### Source

#### ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank – World Development Indicators
Retrieved on: 2025-09-08  
Retrieved from: https://data.worldbank.org/indicator/SL.AGR.EMPL.ZS  


## Industry
Share of total employment working in the industry sector.
Last updated: September 8, 2025  
Next update: September 2026  
Date range: 1991–2023  
Unit: %  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank (2025) – processed by Our World in Data

#### Full citation
ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank (2025) – processed by Our World in Data. “Industry – ILO” [dataset]. ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank, “World Development Indicators 122” [original data].
Source: ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank (2025) – processed by Our World In Data

### What you should know about this data
* Employment refers to all persons of working age who, during a specified brief period, were in paid employment or self-employment.
* The industry sector includes mining and quarrying, manufacturing, electricity, gas, steam and air conditioning supply, water supply, and construction activities, as defined by the [International Standard Industrial Classification of All Economic Activities (ISIC)](https://ilostat.ilo.org/methods/concepts-and-definitions/classification-economic-activities/) (categories B to F in ISIC revision 4).
* This data is part of the ILO Modelled Estimates series. This series combines nationally reported observations with imputed data to have a harmonized, internationally comparable dataset and produce regional and global aggregates. For more information, please refer to the [ILO Modelled Estimates documentation](https://ilostat.ilo.org/methods/concepts-and-definitions/ilo-modelled-estimates/).
* This data is classified according to the 13th International Classification of Labour Statistics (ICLS), where employment includes anyone engaged for at least one hour per day in the production of goods and services, even for own use by the household or family, volunteering, or other forms of unpaid work. For more information, please refer to [this explainer by the International Labour Organization](https://www.ilo.org/publications/quick-guide-understanding-impact-new-statistical-standards-ilostat).

### How is this data described by its producer - ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank (2025)?
Employment is defined as persons of working age who were engaged in any activity to produce goods or provide services for pay or profit, whether at work during the reference period or not at work due to temporary absence from a job, or to working-time arrangement. The industry sector consists of mining and quarrying, manufacturing, construction, and public utilities (electricity, gas, and water), in accordance with divisions 2-5 (ISIC 2) or categories C-F (ISIC 3) or categories B-F (ISIC 4).

### Limitations and exceptions:
There are many differences in how countries define and measure employment status, particularly members of the armed forces, self-employed workers, and unpaid family workers. Where members of the armed forces are included, they are allocated to the service sector, causing that sector to be somewhat overstated relative to the service sector in economies where they are excluded. Where data are obtained from establishment surveys, data cover only employees; thus self-employed and unpaid family workers are excluded. In such cases the employment share of the agricultural sector is severely underreported. Caution should be also used where the data refer only to urban areas, which record little or no agricultural work. Moreover, the age group and area covered could differ by country or change over time within a country. For detailed information, consult the original source.

Countries also take different approaches to the treatment of unemployed people. In most countries unemployed people with previous job experience are classified according to their last job. But in some countries the unemployed and people seeking their first job are not classifiable by economic activity. Because of these differences, the size and distribution of employment by economic activity may not be fully comparable across countries.

The ILO reports data by major divisions of the ISIC revision 2, revision 3, or revision 4. Broad classification such as employment by agriculture, industry, and services may obscure fundamental shifts within countries' industrial patterns. A slight majority of countries report economic activity according to the ISIC revision 3 instead of revision 2 or revision 4. The use of one classification or the other should not have a significant impact on the information for the employment of the three broad sectors data.

### Statistical concept and methodology:
The International Labour Organization (ILO) classifies economic activity using the International Standard Industrial Classification (ISIC) of All Economic Activities, revision 2 (1968), revision 3 (1990), and revision 4 (2008). Because this classification is based on where work is performed (industry) rather than type of work performed (occupation), all of an enterprise's employees are classified under the same industry, regardless of their trade or occupation. The categories should sum to 100 percent. Where they do not, the differences are due to workers who are not classified by economic activity.

The series is part of the "ILO modeled estimates database," including nationally reported observations and imputed data for countries with missing data, primarily to capture regional and global trends with consistent country coverage. Country-reported microdata is based mainly on nationally representative labor force surveys, with other sources (e.g., household surveys and population censuses) considering differences in the data source, the scope of coverage, methodology, and other country-specific factors. Country analysis requires caution where limited nationally reported data are available. A series of models are also applied to impute missing observations and make projections. However, imputed observations are not based on national data, are subject to high uncertainty, and should not be used for country comparisons or rankings. For more information: https://ilostat.ilo.org/resources/concepts-and-definitions/ilo-modelled-estimates/

### Notes from original source:
Given the exceptional situation, including the scarcity of relevant data, the ILO modeled estimates and projections from 2020 onwards are subject to substantial uncertainty.

### Source

#### ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank – World Development Indicators
Retrieved on: 2025-09-08  
Retrieved from: https://data.worldbank.org/indicator/SL.IND.EMPL.ZS  


## Services
Share of total employment working in the services sector.
Last updated: September 8, 2025  
Next update: September 2026  
Date range: 1991–2023  
Unit: %  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank (2025) – processed by Our World in Data

#### Full citation
ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank (2025) – processed by Our World in Data. “Services – ILO” [dataset]. ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank, “World Development Indicators 122” [original data].
Source: ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank (2025) – processed by Our World In Data

### What you should know about this data
* Employment refers to all persons of working age who, during a specified brief period, were in paid employment or self-employment.
* The services sector includes market services (trade, transportation, accommodation and food, and business and administrative services), and non-market services (public administration, community, social, and other services and activities) as defined by the [International Standard Industrial Classification of All Economic Activities (ISIC)](https://ilostat.ilo.org/methods/concepts-and-definitions/classification-economic-activities/) (categories G to U in ISIC revision 4).
* This data is part of the ILO Modelled Estimates series. This series combines nationally reported observations with imputed data to have a harmonized, internationally comparable dataset and produce regional and global aggregates. For more information, please refer to the [ILO Modelled Estimates documentation](https://ilostat.ilo.org/methods/concepts-and-definitions/ilo-modelled-estimates/).
* This data is classified according to the 13th International Classification of Labour Statistics (ICLS), where employment includes anyone engaged for at least one hour per day in the production of goods and services, even for own use by the household or family, volunteering, or other forms of unpaid work. For more information, please refer to [this explainer by the International Labour Organization](https://www.ilo.org/publications/quick-guide-understanding-impact-new-statistical-standards-ilostat).

### How is this data described by its producer - ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank (2025)?
Employment is defined as persons of working age who were engaged in any activity to produce goods or provide services for pay or profit, whether at work during the reference period or not at work due to temporary absence from a job, or to working-time arrangement. The services sector consists of wholesale and retail trade and restaurants and hotels; transport, storage, and communications; financing, insurance, real estate, and business services; and community, social, and personal services, in accordance with divisions 6-9 (ISIC 2) or categories G-Q (ISIC 3) or categories G-U (ISIC 4).

### Limitations and exceptions:
There are many differences in how countries define and measure employment status, particularly members of the armed forces, self-employed workers, and unpaid family workers. Where members of the armed forces are included, they are allocated to the service sector, causing that sector to be somewhat overstated relative to the service sector in economies where they are excluded. Where data are obtained from establishment surveys, data cover only employees; thus self-employed and unpaid family workers are excluded. In such cases the employment share of the agricultural sector is severely underreported. Caution should be also used where the data refer only to urban areas, which record little or no agricultural work. Moreover, the age group and area covered could differ by country or change over time within a country. For detailed information, consult the original source.

Countries also take different approaches to the treatment of unemployed people. In most countries unemployed people with previous job experience are classified according to their last job. But in some countries the unemployed and people seeking their first job are not classifiable by economic activity. Because of these differences, the size and distribution of employment by economic activity may not be fully comparable across countries.

The ILO reports data by major divisions of the ISIC revision 2, revision 3, or revision 4. Broad classification such as employment by agriculture, industry, and services may obscure fundamental shifts within countries' industrial patterns. A slight majority of countries report economic activity according to the ISIC revision 3 instead of revision 2 or revision 4. The use of one classification or the other should not have a significant impact on the information for the employment of three broad sectors data.

### Statistical concept and methodology:
The International Labour Organization (ILO) classifies economic activity using the International Standard Industrial Classification (ISIC) of All Economic Activities, revision 2 (1968), revision 3 (1990), and revision 4 (2008). Because this classification is based on where work is performed (industry) rather than type of work performed (occupation), all of an enterprise's employees are classified under the same industry, regardless of their trade or occupation. The categories should sum to 100 percent. Where they do not, the differences are due to workers who are not classified by economic activity.

The series is part of the "ILO modeled estimates database," including nationally reported observations and imputed data for countries with missing data, primarily to capture regional and global trends with consistent country coverage. Country-reported microdata is based mainly on nationally representative labor force surveys, with other sources (e.g., household surveys and population censuses) considering differences in the data source, the scope of coverage, methodology, and other country-specific factors. Country analysis requires caution where limited nationally reported data are available. A series of models are also applied to impute missing observations and make projections. However, imputed observations are not based on national data, are subject to high uncertainty, and should not be used for country comparisons or rankings. For more information: https://ilostat.ilo.org/resources/concepts-and-definitions/ilo-modelled-estimates/

### Notes from original source:
Given the exceptional situation, including the scarcity of relevant data, the ILO modeled estimates and projections from 2020 onwards are subject to substantial uncertainty.

### Source

#### ILO Modelled Estimates Database (ILOEST), ILOSTAT, via World Bank – World Development Indicators
Retrieved on: 2025-09-08  
Retrieved from: https://data.worldbank.org/indicator/SL.SRV.EMPL.ZS  


    