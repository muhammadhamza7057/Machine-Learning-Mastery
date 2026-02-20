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
    
# Using yield with generator function for fibonacci series Task 05
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Using yield - generator function returns one value at a time
print("Fibonacci Series using yield:")
for num in fibonacci(10):
    print(num, end=" ")
print("\n")

# Lambda with map and yield example
print("Squaring numbers 1-5 using lambda with map:")
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)

# Generator function with yield for even numbers Task 06
def even_numbers(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

print("Even numbers using yield (0-10):")
for even in even_numbers(11):
    print(even, end=" ")
print()
