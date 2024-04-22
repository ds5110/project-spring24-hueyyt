* Data References
 * [FCC National Broadband Map](https://broadbandmap.fcc.gov/data-download/nationwide-data?version=jun2022)
 * [American Community Survey 5-Year Data (2009-2022)](https://www.census.gov/data/developers/data-sets/acs-5year.html)
   Chosen Detailed Tables and Subject Tables. 
   Detailed Tables contain the most detailed cross-tabulations, many of which are published down to block groups. The data are population counts.
    Subject Tables provide an overview of the estimates available in a particular topic.  The data are presented as population counts and percentages. 
 * [Digital Equity Act of 2021 (census.gov)](https://www.census.gov/programs-surveys/community-resilience-estimates/partnerships/ntia/digital-equity.html) includes eight populations: 
    * Persons who are 60 years of age or older
    * Incarcerated individuals
    * Veterans
    * Persons with disabilities
    * Members of a racial or ethnic minority group
    * Rural residents
    * Individuals with a language barrier, including those who are English learners or have low literacy levels
    * Individuals living in households with incomes not exceeding 150 percent of the poverty level


make -f Makefile data
This will download data.


make -f Makefile speed
This is for calculate average downlaod and upload speed

make -f Makefile population
For calculate percentage of populaiton can't access to network or compute device.

make -f Makefile INFA
To calculate INFA 

make -f Makefile maps
To combine INFA and geo data and make maps by geo id.

INFA MAP:
![01](img/INFA_scaled_tract.png)
This is a test map for using code and visualize data, not final version. Since we found several different equations and data. 




* Data Use
 * Persons who are 60 years of age or older(subject table)
   Topics: Population and People -> Age and Sex 
   -> Total population -> SELECTED AGE CATEGORIES
   S0101_C01_028E

    ```
    0	Over 60 Pop	state	 county	 tract
    1	        542	   23	   001	010100
    2	       1291	   23	   001	010200
    3	        641	   23	   001	010300
    4	        832	   23	   001	010400
    ```

 * Incarcerated individuals(detailed table)
   Topics: Population and People -> Count, Estimates, and Projections -> Group Quarters Population -> B26103 Group Quarters Type -> Adult correctional facilities
   B26103_004E

    ```
    0	Incarcerated individuals   state 	county	 tract
    1	                    None	23	  001	  010100
    2	                    None	23	  001	  010200
    3	                    None	23	  001	  010300
    4	                    None	23	  001	  010400
    ```

 * Veterans(detailed table)
   Topics: Population and People ->Veterans
   B21001_002E

    ```
    0	Veterans	state	 county	 tract
    1	      95	   23	   001	010100
    2	     408	   23	   001	010200
    3	     173	   23	   001	010300
    4	     144	   23	   001	010400
    ```
   
 * Persons with disabilities(subject table)
   Topics: Health -> Disability
   S1810_C01_001E

    ```
    0	Disabled	state	 county	  tract
    1	     535	   23	   001	  010100
    2	     969	   23	   001	  010200
    3	     804	   23	   001	  010300
    4	     291	   23	   001	  010300
    ```





## Members of a racial or ethnic minority group
_(def)_ The population who identify as a race other than White alone or as Hispanic or Latino of any
race

Below is an overview of the population data about members of a racial or ethnic minority group.
```
Members of a racial or ethnic minority group
0 TOTAL_POP  MINORITY_POP           ID
0      1538           197  23001010100
1      5149           186  23001010200
2      2554           407  23001010300
3      2245           191  23001010400
4      2295           339  23001010500
```

## TODO: Rural residents
_(def)_ The rural population, as defined by the Digital Equity Act of 2021, is the population living
outside of cities and towns with more than 20,000 residents or living outside larger cities and
towns with more than 50,000 residents and their surrounding urban areas.

Below is an overview of the population data about rural residents in 2020 Demographic and Housing Characteristics Table. 
```
Rural residents
0                                          NAME TOTAL_POP URBAN_POP RURAL_POP           ID
0  Census Tract 101; Androscoggin County; Maine      1006      1006         0  23001010100
1  Census Tract 102; Androscoggin County; Maine      2243      1564       679  23001010200
2  Census Tract 103; Androscoggin County; Maine      1216      1216         0  23001010300
3  Census Tract 104; Androscoggin County; Maine       845       845         0  23001010400
4         Census Tract 9901; York County; Maine         0         0         0  23031990100
```

## Individuals with a language barrier
_(def)_ English learners or have low literacy levels. English learners are defined as individuals who
speak a language other than English at home and speak English less than “very well.”

Below is an overview of the population data about individuals with a language barrier.
```
Individuals with a language barrier
0  LANG_POP           ID
0       101  23001010100
1        62  23001010200
2        60  23001010300
3        53  23001010400
4        80  23001010500
```
## Individuals with incomes not exceeding 150 percent of the poverty level
_(def)_ Households with income no more than 150 percent of the federal poverty threshold.

Below is an overview of the population data about individuals with incomes not exceeding 150 percent of the poverty level.
```
Individuals with incomes not exceeding 150 percent of poverty level
0 POVERTY_POP           ID
0         777  23001010100
1         667  23001010200
2         515  23001010300
3         371  23001010400
4         657  23001010500
```

## Cleaned Table
The following table is an overview of the last four covered populations.
```
The covered populations - last four groups
Number of unique ID: 407
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 407 entries, 0 to 406
Data columns (total 5 columns):
 #   Column        Non-Null Count  Dtype
---  ------        --------------  -----
 0   TOTAL_POP     407 non-null    int64
 1   MINORITY_POP  407 non-null    int64
 2   ID            407 non-null    object
 3   LANG_POP      407 non-null    int64
 4   POVERTY_POP   407 non-null    int64
dtypes: int64(4), object(1)
memory usage: 16.0+ KB
None
0  TOTAL_POP  MINORITY_POP           ID  LANG_POP  POVERTY_POP
0       1538           197  23001010100       101          777
1       5149           186  23001010200        62          667
2       2554           407  23001010300        60          515
3       2245           191  23001010400        53          371
4       2295           339  23001010500        80          657
```

Below is the distribution. 
<img src="img/covered_pop_last_4_scatter.png">

## Discussion
- Based on the histograms, data is highly skewed. 

## Future work
- Rural residents data is incomplete because rural residents data (2018-2022) can not be found. [H2 Urban and Rural Table](https://data.census.gov/table/DECENNIALDHC2020.H2?q=rural&g=040XX00US23$1400000) might be added but it only contains data in 2020. 
- Individuals with low literacy levels are not included. Data needs to be added from National Center for Education Statistics. 
- Data need to be saved as .csv file after collecting all necessary data.