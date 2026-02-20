from abc import ABC, abstractmethod
import math

# 🔷 Base Abstract Class
class Shape(ABC):

    @abstractmethod
    def calculate_area(self):
        pass


# 🔷 Rectangle Class
class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def calculate_area(self):
        return self.length * self.width


# 🔷 Square Class
class Square(Shape):
    def __init__(self, side):
        self.side = side

    def calculate_area(self):
        return self.side ** 2


# 🔷 Circle Class
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def calculate_area(self):
        return math.pi * (self.radius ** 2)


# 🔷 Cylinder Class (Surface Area)
class Cylinder(Shape):
    def __init__(self, radius, height):
        self.radius = radius
        self.height = height

    def calculate_area(self):
        return 2 * math.pi * self.radius * (self.radius + self.height)


# ✅ Testing the Classes
rectangle = Rectangle(10, 5)
square = Square(4)
circle = Circle(3)
cylinder = Cylinder(3, 7)

print("Rectangle Area:", rectangle.calculate_area())
print("Square Area:", square.calculate_area())
print("Circle Area:", circle.calculate_area())
print("Cylinder Surface Area:", cylinder.calculate_area())
