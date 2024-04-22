# Allows use of make data while having a data folder
.PHONY: data img

all: clean-data data img speed avg json state block DDI
# Creates the data folder
data:
	mkdir -p data
	cd data; curl -LO https://www2.census.gov/geo/tiger/TIGER2023/TABBLOCK20/tl_2023_78_tabblock20.zip
	cd data; curl -LO https://raw.githubusercontent.com/hueyyt/INFA/main/bdc_23_Cable_fixed_broadband_J23_05mar2024.zip
	cd data; curl -LO https://raw.githubusercontent.com/hueyyt/INFA/main/bdc_23_Copper_fixed_broadband_J23_05mar2024.zip
	cd data; curl -LO https://raw.githubusercontent.com/hueyyt/INFA/main/bdc_23_FibertothePremises_fixed_broadband_J23_05mar2024.zip
	cd data; curl -LO https://raw.githubusercontent.com/hueyyt/INFA/main/bdc_23_LicensedFixedWireless_fixed_broadband_J23_05mar2024.zip
	cd data; curl -LO https://raw.githubusercontent.com/hueyyt/INFA/main/ACSST5Y2022.S2802-Data.csv

img:
	mkdir -p img

speed:
	python3 -B src/speed.py

population:
	python3 -B src/population.py

INFA:
	python3 -B src/INFA.py

maps:
	python3 -B src/maps.py

# estimate rural residents
rural_est:
	mkdir -p data
	python -B src/rural_est.py

# calculate SE score
SE:
	python -B src/SE.py
# visualize SE score
SE_map:
	python -B src/SE_map.py

# analyze SE score
analysis:
	python -B src/analysis.py

DDI:
	python -B src/DDI.py

DDI_map:
	python -B src/DDI_map.py

clean-data:
	rm -rf data

