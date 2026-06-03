import numpy as np
array = np.random.rand(8)
print("Original:", array)
normalized = array * 100
print("Normalized:", normalized)
filtered = normalized[normalized > 50]
print("Filtered (>50):", filtered)
sorted_values = np.sort(filtered)
print("Sorted filtered values:", sorted_values)