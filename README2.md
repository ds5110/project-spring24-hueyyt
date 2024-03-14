# project-spring24 -- MCA

Used Data: INFA, SE

* Data References
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
    Here is the previous four data and 

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
    0	Incarcerated individuals	state	county	tract
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
    4      291	   23	   001	  010400
   ```

   