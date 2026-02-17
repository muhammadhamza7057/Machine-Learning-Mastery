import sys
print(sys.version)
print("This is Muhammad Hamza Software Engineer")
if 5 > 3:
    print("5 is greater than 3")
else :
    print("5 is not greater than 3")

    #This is the muhammad hamza
    #This is the software engineer
print("Hello World!")
print("Have a good day.")
print("Learning Python is fun!")

print("Hello"); print("How are you?"); print("Bye bye!")

print("Hello World!")
print("I will print on the same line.")

x = 5
y = "Hamza"
print("This is the number : " + str(x))
print("This is the name : " + y)


print(type(x))
print(type(y))

x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)


import random

print(random.randrange(1, 10))
 #string iteration 
for x in "banana":
  print(x)
#Check if "expensive" is NOT present in the string:
  txt = "The best things in life are free!"
if "expensive" not in txt:
  print("No, 'expensive' is NOT present.")
if "life" in txt:
  print("Yes, 'life' is present.")

  #this is the concetatntion in python 
  a = "Hello"
b = "World"
c = a + " " + b
print(c)

# Arithmetic operators (+, -, *, /, %, **, //)
# Assignment operators (=, +=, -=, *=, /=, %=, **=, //=)
# Comparison operators (==, !=, >, <, >=, <=)
# Logical operators (and, or, not)
# Identity operators (is, is not)
# Membership operators (in, not in)
# Bitwise operators (&, |, ^, ~, <<, >>)

g = 10
h = 5
print(g + h)  # Addition
print(g - h)  # Subtraction
print(g * h)  # Multiplication
print(g / h)  # Division
print(g % h)  # Modulus
print(g ** h) # Exponentiation
print(g // h) # Floor division
if(g > h and g != h):
    print("g is greater than h and they are not equal.")
if(g > h or g == h):
    print("g is greater than h or they are equal.")

    fruits = ("apple", "banana", "cherry")

    thistuple = ("apple", "banana", "cherry")
i = 0
while i < len(thistuple):
  print(thistuple[i])
  i = i + 1

  fruits = ('apple', 'banana', 'cherry')
(x, *y) = fruits
print(y)