# Methodology

## Purdue Digital Divide Index (DDI)

We started with the [Purdue Digital Divide Index](https://storymaps.arcgis.com/stories/8ad45c48ba5c43d8ad36240ff0ea0dc7) and [DS5010](https://github.com/ds5010/broadband-3/tree/main). We choose the FCC in DS5010 rather than Ookla Speedtest(R)  results in Purdue Index.

We keep the same data soure with DS5010 but update the data by 2023 version. We use the maximum of download/upload max speeds offered by providers of broadband cable, copper, fiber, and licensed fixed wireless in each census sub-block. Then we averaged those for each census tract.

We also update the Geography Data with 2023 version from [Census](https://www2.census.gov/geo/tiger/TIGER2023/TABBLOCK20/tl_2023_78_tabblock20.zip)

Like Purdue and DS5010, our population data came from [American Community Survey 5-Year Data (2022)](https://www.census.gov/data/developers/data-sets/acs-5year.html) but we update it by 2022 version and use different factors according to [Digital Equity Act of 2021 (census.gov)](https://www.census.gov/programs-surveys/community-resilience-estimates/partnerships/ntia/digital-equity.html) includes eight populations: 
    * Persons who are 60 years of age or older
    * Incarcerated individuals
    * Veterans
    * Persons with disabilities
    * Members of a racial or ethnic minority group
    * Rural residents
    * Individuals with a language barrier, including those who are English learners or have low literacy levels
    * Individuals living in households with incomes not exceeding 150 percent of the poverty level
    



### Calculation

* INFA = NIA*0.3 + NCD*0.3 – DNS*0.05 – UPS*0.05
* SE = AGE60 + INCAR + VET + DIS + MIN + RURAL + LANG + POV 
* DDI = INFA + SE

#### INFA (Infrastructure/adoption)
* NIA: z-scores of the percent of population with no internet access(NIA)
* NCD: z-scores of the percent of population with no computing devices (NCD)
* DNS: z-scores of the average max download available (DNS)
* UPS: z-scores of the average max upload available (UPS)

#### SE (Socioeconomic)
* AGE65: z-scores of the percent population who are 60 years of age or older
* INCAR: z-scores of the percent Incarcerated individuals
* VET: z-scores of the percent Veterans
* DIS: z-scores of percent noninstutionalized population with any disability (DIS)
* MIN: z-scores of the percent  Members of a racial or ethnic minority group
* RURAL: z-scores of the percent Rural residents
* LANG: z-scores of the percent Individuals with a language barrier, including those who are English learners or have low literacy levels
* POV: z-scores of Individuals living in households with incomes not exceeding 150 percent of the poverty level





## Resources

#### FCC Internet Speeds
* [FCC National Broadband Map](https://broadbandmap.fcc.gov/data-download/nationwide-data?version=jun2023)

#### Geography Data
* [Shapefiles from the US Census Bureau](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)
* [The specific file that we used from the Census](https://www2.census.gov/geo/tiger/TIGER2023/TABBLOCK20/tl_2023_78_tabblock20.zip)

#### Purdue DDI Information
* [Purdue Digital Divide Index](https://storymaps.arcgis.com/stories/8ad45c48ba5c43d8ad36240ff0ea0dc7)
* [Purdue DDI Additional Info](https://pcrd.purdue.edu/ruralindianastats/broadband/ddi.php?variable=ddi-overview&county=Adams)

#### American Community Survey - 5 Year - 2022
* [ACS 5 Main Page](https://www.census.gov/data/developers/data-sets/acs-5year.html)