import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
n = 100  
k_true = 2 
b_true = 1 
x = np.linspace(0, 10, n)
y = k_true * x + b_true + np.random.normal(0, 1, n)  


def mean_squared_error(k, b, x, y):
    y_mean = b + k*x
    return np.sum((y - y_mean) ** 2)/len(x)

def gradient_descent(x, y, k_init, b_init, learning_rate, n_iter):
    k = k_init
    b = b_init
    errors = []

    for _ in range(n_iter):
        y_mean = b + k*x

        grad_k = -(2 / len(x)) * np.sum(x*(y - y_mean))
        grad_b = -(2 / len(x)) * np.sum(y - y_mean)
        
        k -= learning_rate * grad_k
        b -= learning_rate * grad_b

        error = mean_squared_error(k, b, x, y)
        errors.append(error)

    return k, b, errors


learning_rate = 0.01
n_iter = 1000
k_init = 0  
b_init = 0 


k_gd, b_gd, errors = gradient_descent(x, y, k_init, b_init, learning_rate, n_iter)
y_gd = k_gd * x + b_gd


k_polyfit, b_polyfit = np.polyfit(x, y, 1)

plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', label='Data')

plt.plot(x, y_gd, color='red', label=f'Gradient Descent: k = {k_gd:.2f}, b = {b_gd:.2f}')

y_polyfit = k_polyfit * x + b_polyfit
plt.plot(x, y_polyfit, color='green', label=f'np.polyfit: k = {k_polyfit:.2f}, b = {b_polyfit:.2f}')

y_true = k_true * x + b_true
plt.plot(x, y_true, color='purple', linestyle='--', label=f'True Line: k = {k_true}, b = {b_true}')

plt.title("Linear Regression: Gradient Descent vs np.polyfit")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(errors, color='orange')
plt.title("Error vs Iterations (Gradient Descent)")
plt.xlabel("Iterations")
plt.ylabel("Mean Squared Error (MSE)")
plt.grid(True)
plt.show()

print(f"True Parameters: k = {k_true}, b = {b_true}")
print(f"Gradient Descent Parameters: k = {k_gd:.2f}, b = {b_gd:.2f}")
print(f"np.polyfit Parameters: k = {k_polyfit:.2f}, b = {b_polyfit:.2f}")
