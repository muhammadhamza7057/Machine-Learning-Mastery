# The Lamda Function Task 02
def square(x):
    return x * x   
print(square(5))

# The Task 03 is also here
number = lambda b: b * b
print(number(3))


# Using the for loop to print from 1 to 100 random numbers Task 04
import random
for i in range(1, 5):
    print(random.randint(1, 100))
    
# Using the for loop that return fibonacci series Task 05
def fibonacci(n):
    fib_series = []
    a, b = 0, 1
    for _ in range(n):
        fib_series.append(a)
        a, b = b, a + b
    return fib_series
print(fibonacci(10))
