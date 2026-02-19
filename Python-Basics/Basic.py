"""
===============================================
PYTHON BASICS - COMPLETE LEARNING GUIDE
===============================================
This file covers fundamental Python concepts.
Each section builds on previous knowledge.
Run this file to see all concepts in action.
===============================================
"""

import sys
import random

# ============================================
# 1. PYTHON VERSION & SYSTEM INFORMATION
# ============================================
print("=" * 50)
print("1. PYTHON VERSION & SYSTEM INFO")
print("=" * 50)
print(f"Python Version: {sys.version}")
print("This is Muhammad Hamza - Software Engineer\n")


# ============================================
# 2. CONDITIONAL STATEMENTS (IF-ELSE)
# ============================================
print("=" * 50)
print("2. CONDITIONAL STATEMENTS")
print("=" * 50)

# Basic if-else structure: checks if a condition is True or False
if 5 > 3:
    print("✓ 5 is greater than 3  (condition is TRUE)")
else:
    print("✗ 5 is not greater than 3  (condition is FALSE)")
print()


# ============================================
# 3. PRINT STATEMENTS & OUTPUT
# ============================================
print("=" * 50)
print("3. PRINT STATEMENTS - BASIC OUTPUT")
print("=" * 50)

# Single print statements
print("Hello World!")
print("Have a good day.")
print("Learning Python is fun!")

# Multiple statements on one line (use semicolon) - Note: Generally not recommended
print("Multiple statements on one line:  ", end="")
print("Hello"); print("How are you?"); print("Bye bye!")
print()


# ============================================
# 4. VARIABLES & DATA TYPES
# ============================================
print("=" * 50)
print("4. VARIABLES & DATA TYPES")
print("=" * 50)

# Variables store data. Python is dynamically typed (no need to declare types)
num_value = 5          # Integer
name_value = "Hamza"   # String

print(f"Number value: {num_value} (type: {type(num_value).__name__})")
print(f"Name value: {name_value} (type: {type(name_value).__name__})")

# String concatenation: combining strings together
combined = "This is the number: " + str(num_value) + " and the name: " + name_value
print(combined)
print()


# ============================================
# 5. MULTIPLE ASSIGNMENT (UNPACKING)
# ============================================
print("=" * 50)
print("5. MULTIPLE ASSIGNMENT - UNPACKING VARIABLES")
print("=" * 50)

# Assign multiple values to multiple variables at once
fruit1, fruit2, fruit3 = "Orange", "Banana", "Cherry"
print(f"Unpacking fruits: {fruit1}, {fruit2}, {fruit3}")
print()


# ============================================
# 6. RANDOM NUMBER GENERATION
# ============================================
print("=" * 50)
print("6. RANDOM NUMBER GENERATION")
print("=" * 50)

# Generate a random integer between 1 and 9 (inclusive)
random_num = random.randrange(1, 10)
print(f"Random number between 1-9: {random_num}")
print()


# ============================================
# 7. STRING ITERATION (LOOPS)
# ============================================
print("=" * 50)
print("7. STRING ITERATION - FOR LOOPS")
print("=" * 50)

# Iterate through each character in a string
print("Iterating through characters in 'banana':")
for char in "banana":
    print(f"  {char}")
print()


# ============================================
# 8. MEMBERSHIP OPERATORS (IN, NOT IN)
# ============================================
print("=" * 50)
print("8. MEMBERSHIP OPERATORS - CHECKING IF ITEM EXISTS")
print("=" * 50)

text = "The best things in life are free!"

# Check if a word is NOT in the string
if "expensive" not in text:
    print("✓ 'expensive' is NOT present in the text")

# Check if a word IS in the string
if "life" in text:
    print("✓ 'life' IS present in the text")
print()


# ============================================
# 9. STRING CONCATENATION
# ============================================
print("=" * 50)
print("9. STRING CONCATENATION - JOINING STRINGS")
print("=" * 50)

# Method 1: Using the + operator
greeting_part1 = "Hello"
greeting_part2 = "World"
full_greeting = greeting_part1 + " " + greeting_part2
print(f"Concatenated string: {full_greeting}")
print()


# ============================================
# 10. ARITHMETIC OPERATORS
# ============================================
print("=" * 50)
print("10. ARITHMETIC OPERATORS - MATH OPERATIONS")
print("=" * 50)

num1 = 10
num2 = 5

print(f"{num1} + {num2} = {num1 + num2}       (Addition)")
print(f"{num1} - {num2} = {num1 - num2}       (Subtraction)")
print(f"{num1} * {num2} = {num1 * num2}       (Multiplication)")
print(f"{num1} / {num2} = {num1 / num2}       (Division - returns float)")
print(f"{num1} % {num2} = {num1 % num2}       (Modulus - remainder)")
print(f"{num1} ** {num2} = {num1 ** num2}     (Exponentiation - power)")
print(f"{num1} // {num2} = {num1 // num2}     (Floor Division - rounds down)")
print()


# ============================================
# 11. COMPARISON & LOGICAL OPERATORS
# ============================================
print("=" * 50)
print("11. COMPARISON & LOGICAL OPERATORS")
print("=" * 50)

g = 10
h = 5

# Logical AND: both conditions must be TRUE
if (g > h and g != h):
    print("✓ g is GREATER than h AND they are NOT equal (AND operator)")

# Logical OR: at least one condition must be TRUE
if (g > h or g == h):
    print("✓ g is GREATER than h OR they are equal (OR operator)")
print()


# ============================================
# 12. TUPLES - ORDERED, IMMUTABLE COLLECTIONS
# ============================================
print("=" * 50)
print("12. TUPLES - ORDERED, IMMUTABLE COLLECTIONS")
print("=" * 50)

# Tuples are created with parentheses, items cannot be changed after creation
fruits_tuple = ("apple", "banana", "cherry")
print(f"Tuple: {fruits_tuple}")
print(f"Length of tuple: {len(fruits_tuple)}")

# Accessing tuple items using index (0-based indexing)
print("Iterating through tuple using while loop:")
index = 0
while index < len(fruits_tuple):
    print(f"  Index {index}: {fruits_tuple[index]}")
    index = index + 1
print()


# ============================================
# 13. TUPLE UNPACKING
# ============================================
print("=" * 50)
print("13. TUPLE UNPACKING - ADVANCED")
print("=" * 50)

# Unpack tuple with * operator: * captures remaining items in a list
fruits_for_unpacking = ('apple', 'banana', 'cherry')
first_fruit, *remaining_fruits = fruits_for_unpacking
print(f"First fruit: {first_fruit}")
print(f"Remaining fruits: {remaining_fruits}")
print()


# ============================================
# 14. SETS - UNORDERED, UNINDEXED COLLECTIONS
# ============================================
print("=" * 50)
print("14. SETS - UNORDERED, UNINDEXED COLLECTIONS")
print("=" * 50)

# Sets are created with curly braces, items are unique and unordered
my_set = {"apple", "banana", "cherry"}
print(f"Original set: {my_set}")
print(f"Length of set: {len(my_set)}")

# Add a single item to the set
my_set.add("orange")
print(f"After adding 'orange': {my_set}")

# Update set with multiple items (pass an iterable like a list)
my_set.update(["mango", "grapes"])
print(f"After updating with ['mango', 'grapes']: {my_set}")

# Remove an item from the set
my_set.remove("banana")
print(f"After removing 'banana': {my_set}")

# Iterate through set items
print("Iterating through set:")
for fruit in my_set:
    print(f"  - {fruit}")
print()



# ============================================
# 15. FROZENSETS - IMMUTABLE SETS
# ============================================
print("=" * 50)
print("15. FROZENSETS - IMMUTABLE SETS")
print("=" * 50)

print("WHAT IS A FROZENSET?")
print("-" * 50)
print("• Frozenset is an immutable (unchangeable) version of a set")
print("• Items are unique and unordered (like sets)")
print("• Cannot add, remove, or modify items after creation")
print("• Can be used as dictionary keys (unlike regular sets)")
print()

print("USE CASES:")
print("-" * 50)
print("✓ Recommendation systems ('Customers who bought also bought...')")
print("✓ Machine Learning - Association rule mining (Apriori algorithm)")
print("✓ Caching and hashing - when you need immutable collections")
print("✓ Using sets as dictionary keys or in other sets")
print()

# Create a frozenset
fruits_frozenset = frozenset({"apple", "banana", "cherry"})
print(f"Created frozenset: {fruits_frozenset}")
print(f"Type: {type(fruits_frozenset)}")
print()

# Demonstrate immutability - can check membership
print("Checking if items exist in frozenset:")
print(f"'apple' in frozenset: {'apple' in fruits_frozenset}")
print(f"'grapes' in frozenset: {'grapes' in fruits_frozenset}")
print()

# Convert frozenset to list
print(f"Convert to list: {list(fruits_frozenset)}")
print()

# Use frozenset as dictionary key (cannot use regular set)
print("Using frozenset as dictionary key:")
recommendations = {
    frozenset(["pizza", "coke"]): ["burger", "fries"],
    frozenset(["laptop", "mouse"]): ["keyboard", "monitor"]
}
print(f"Recommendations dictionary: {recommendations}")
print()

print("=" * 50)
print("END OF PYTHON BASICS GUIDE")
print("=" * 50)