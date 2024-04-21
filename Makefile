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
SE_analysis:
	python -B src/SE_analysis.py


