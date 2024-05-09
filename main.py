import numpy as np

arr = np.arange(12).reshape(2, 3, 2)

print(arr)

print(arr.shape)

print(arr.min(0))

print(arr.min(1))

print(arr.min(2))