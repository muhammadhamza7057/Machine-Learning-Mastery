from abc import ABC, abstractmethod
import math


class Shape(ABC):
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def calculate_area(self):
        pass
    
    def describe(self):
        return f"{self.name} is a shape"
    



class Rectangle(Shape):
    def __init__(self, length, width):
        super().__init__("Rectangle")
        self.length = length
        self.width = width

    def calculate_area(self):
        return self.length * self.width


class Square(Shape):
    def __init__(self, side):
        super().__init__("Square")
        self.side = side

    def calculate_area(self):
        return self.side ** 2



class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def calculate_area(self):
        return math.pi * (self.radius ** 2)


class Cylinder(Shape):
    def __init__(self, radius, height):
        super().__init__("Cylinder")
        self.radius = radius
        self.height = height

    def calculate_area(self):
        return 2 * math.pi * self.radius * (self.radius + self.height)



rectangle = Rectangle(10, 5)
square = Square(4)
circle = Circle(3)
cylinder = Cylinder(3, 7)

# Using super() - the parent class's methods are now properly initialized
print("--- Shape Descriptions (using super() initialization) ---")
print(rectangle.describe())
print(square.describe())
print(circle.describe())
print(cylinder.describe())

print("\n--- Area Calculations ---")
print("Rectangle Area:", rectangle.calculate_area())
print("Square Area:", square.calculate_area())
print("Circle Area:", circle.calculate_area())
print("Cylinder Surface Area:", cylinder.calculate_area())
