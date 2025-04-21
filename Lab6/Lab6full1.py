import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
n = 100 
k_true = 1 
b_true = 4 
x = np.linspace(0, 10, n)
y = k_true * x + b_true + np.random.normal(0, 1, n) 

def least_squares(x, y):
    k = np.sum((x - np.mean(x)) * (y - np.mean(y))) / np.sum((x - np.mean(x))**2)
    b = np.mean(y) - k * np.mean(x)
    return k, b

k_ls, b_ls = least_squares(x, y)

k_polyfit, b_polyfit = np.polyfit(x, y, 1)


plt.figure(figsize=(10, 6))

plt.scatter(x, y, color='blue', label='Data')

y_ls = k_ls * x + b_ls
plt.plot(x, y_ls, color='red', label=f'Least Squares: k = {k_ls:.2f}, b = {b_ls:.2f}')


y_polyfit = k_polyfit * x + b_polyfit
plt.plot(x, y_polyfit, color='green', label=f'np.polyfit: k = {k_polyfit:.2f}, b = {b_polyfit:.2f}')


y_true = k_true * x + b_true
plt.plot(x, y_true, color='purple', linestyle='--', label=f'True Line: k = {k_true}, b = {b_true}')


plt.title("Linear Regression: Least Squares vs np.polyfit")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()

print(f"True Parameters: k = {k_true}, b = {b_true}")
print(f"Least Squares Parameters: k = {k_ls:.2f}, b = {b_ls:.2f}")
print(f"np.polyfit Parameters: k = {k_polyfit:.2f}, b = {b_polyfit:.2f}")
