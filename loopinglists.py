import math
raw_data = [56.2, float('NaN'), 51.7, 55.3, 52.5, float('NaN'), 47.8, 3.5,-2.7]
filtered_data = []
for value in raw_data:
    if (not math.isnan(value) and value >= 0):
        filtered_data.append(value)

print(filtered_data)
