# calculate SE score
SE:
	mkdir -p data
	python -B src/SE.py
# visualize SE score
SE_map:
	python -B src/SE_map.py


