from abc import ABC, abstractmethod
from math import asin, acos, pi, tan
import turtle


# turtle settings
def setTurtle(w):
    t = turtle.Turtle()
    screen = t.getscreen()
    screen.screensize(canvwidth=3*w, canvheight=3*w)
    t.fillcolor("yellow")
    t.shape("turtle")
    t.speed(1)
    t.pensize(5)
    t.pencolor("white")
    t.setpos(-100, -150)
    t.pencolor("black")
    return t

# Parent Class
class Polygon(ABC):

    def __init__(self, sides, regular):
        self.regular = regular
        self.sides = sides
        self.nosides = len(sides)
        if self.regular:
            self.side = self.sides[0]
            self.angle = ((self.nosides - 2) * 180) / self.nosides

    def area(self):
        n = self.nosides
        l = self.side
        return (l**2 * n)/(4 * tan(pi/n))

    def perimeter(self):
        return sum(self.sides)

    @abstractmethod
    def Draw(self):
        pass


# Child Classes
class Triangle(Polygon):

    def __init__(self, sides, regular=False):
        super().__init__(sides, regular)
        self.angle1 = 180 - \
            (180/pi) * acos((sides[2]**2-sides[0] **
                             2-sides[1]**2)/(-2*(sides[0]*sides[1])))
        self.angle2 = 180 - \
            (180/pi) * acos((sides[0]**2-sides[1] **
                             2-sides[2]**2)/(-2*(sides[1]*sides[2])))

    def area(self):
        s = sum(self.sides)/2
        return (s * (s - self.sides[0])*(s - self.sides[1])*(s - self.sides[2]))**0.5

    def Draw(self):
        t = setTurtle(self.sides[0])
        t.forward(self.sides[0])
        t.left(self.angle1)
        t.forward(self.sides[1])
        t.left(self.angle2)
        t.forward(self.sides[2])
        turtle.done()


class Quad(Polygon):

    def __init__(self, sides, regular=False):
        super().__init__(sides, regular)

    def area(self):
        return self.sides[0] * self.sides[1]

    def Draw(self):
        t = setTurtle(self.sides[0])
        for i in range(2):
            t.forward(self.sides[0])
            t.left(90)
            t.forward(self.sides[1])
            t.left(90)
        turtle.done()


class Pent(Polygon):

    def __init__(self, side):
        self.side = side
        sides = [side for i in range(5)]
        super().__init__(sides, True)

    def Draw(self):
        t = setTurtle(self.side)
        for i in range(5):
            t.forward(self.side)
            t.left(180-self.angle)
        turtle.done()


class Hex(Polygon):

    def __init__(self, side):
        self.side = side
        sides = [side for i in range(6)]
        super().__init__(sides, True)

    def Draw(self):
        t = setTurtle(self.side)
        for i in range(6):
            t.forward(self.side)
            t.left(180-self.angle)
        turtle.done()


class Oct(Polygon):

    def __init__(self, side):
        self.side = side
        sides = [side for i in range(8)]
        super().__init__(sides, True)

    def Draw(self):
        t = setTurtle(self.side)
        for i in range(8):
            t.forward(self.side)
            t.left(180-self.angle)
        turtle.done()


class Isos(Triangle):

    def __init__(self, base, side):
        sides = [base, side, side]
        super().__init__(sides)


class Equi(Triangle):

    def __init__(self, side):
        sides = [side for i in range(3)]
        super().__init__(sides, True)


class Rect(Quad):

    def __init__(self, width, height):
        sides = [width, height, width, height]
        super().__init__(sides)


class Square(Quad):

    def __init__(self, side):
        sides = [side for i in range(4)]
        super().__init__(sides, True)


# function to get numerical inputs
def innumber(statement):
    while True:
        try:
            l = int(input(statement))
            if l >= 1:
                break
            else:
                print("length should be a positive integer")
                continue
        except:
            print("length should be a positive integer")
            continue
    return l


# function to get different actions
def action():
    print("Calculate Area: a - Calculate Perimeter: p - Draw Shape: d")
    act = input("Enter a character representing an action: ")
    while act != 'a' and act != 'p' and act != 'd':
        print("please enter a valid action")
        print("Calculate Area: a - Calculate Perimeter: p - Draw Shape: d")
        act = input("Enter a character representing an action: ")
    return act


# choose basic shape
print("Triangle: t - Quadrilateral: q - Pentagon: p - Hexagon: h - Octagon: o")
shape = input("Enter a character representing a shape: ")
while shape != 't' and shape != 'q' and shape != 'p' and shape != 'h' and shape != 'o':
    print("please enter a valid shape")
    print("Triangle: t - Quadrilateral: q - Pentagon: p - Hexagon: h - Octagon: o")
    shape = input("Enter a character representing a shape: ")


# choose type of triangle
if shape == 't':
    print("Equilateral: e - Isosceles: i - Scalene: s")
    shape = input("Enter a character representing a triangle: ")
    while shape != 'e' and shape != 'i' and shape != 's':
        print("please enter a valid triangle")
        print("Equilateral: e - Isosceles: i - Scalene: s")
        shape = input("Enter a character representing a triangle: ")
    if shape == 'e':
        side = innumber("Enter the side length of the triangle: ")
        act = action()
        if act == 'a':
            print(f"The Area = {Equi(side).area()}")
        elif act == 'p':
            print(f"The Perimeter = {Equi(side).perimeter()}")
        else:
            Equi(side).Draw()
    elif shape == 'i':
        base = innumber("Enter the base length of the triangle: ")
        side = innumber("Enter the side length of the triangle: ")
        while (base + base <= side or side + base <= base):
            print("The lengths entered cannot form a real triangle")
            base = innumber("Enter the base length of the triangle: ")
            side = innumber("Enter the side length of the triangle: ")
        act = action()
        if act == 'a':
            print(f"The Area = {Isos(base, side).area()}")
        elif act == 'p':
            print(f"The Perimeter = {Isos(base, side).perimeter()}")
        else:
            Isos(base, side).Draw()
    else:
        side1 = innumber("Enter the first side length of the triangle: ")
        side2 = innumber("Enter the second side length of the triangle: ")
        side3 = innumber("Enter the third side length of the triangle: ")
        while (side1 + side2 <= side3 or side1 + side3 <= side2 or side2 + side3 <= side1):
            print("The three lengths cannot form a real triangle")
            side1 = innumber("Enter the first side length of the triangle: ")
            side2 = innumber("Enter the second side length of the triangle: ")
            side3 = innumber("Enter the third side length of the triangle: ")
        act = action()
        if act == 'a':
            print(f"The Area = {Triangle([side1,side2,side3]).area()}")
        elif act == 'p':
            print(
                f"The Perimeter = {Triangle([side1,side2,side3]).perimeter()}")
        else:
            Triangle([side1, side2, side3]).Draw()


# choose type of quadrilateral
elif shape == 'q':
    print("Square: s - Rectangle: r")
    shape = input("Enter a character representing a quadrilateral: ")
    while shape != 's' and shape != 'r':
        print("please enter a valid quadrilateral")
        print("Square: s - Rectangle: r")
        shape = input("Enter a character representing a quadrilateral: ")
    if shape == 's':
        side = innumber("Enter the side length of the square: ")
        act = action()
        if act == 'a':
            print(f"The Area = {Square(side).area()}")
        elif act == 'p':
            print(f"The Perimeter = {Square(side).perimeter()}")
        else:
            Square(side).Draw()
    elif shape == 'r':
        width = innumber("Enter the width of the rectangle: ")
        height = innumber("Enter the height of the rectangle: ")
        act = action()
        if act == 'a':
            print(f"The Area = {Rect(width, height).area()}")
        elif act == 'p':
            print(f"The Perimeter = {Rect(width, height).perimeter()}")
        else:
            Rect(width, height).Draw()


# pentagon
elif shape == 'p':
    side = innumber("Enter the side length of the pentagon: ")
    act = action()
    if act == 'a':
        print(f"The Area = {Pent(side).area()}")
    elif act == 'p':
        print(f"The Perimeter = {Pent(side).perimeter()}")
    else:
        Pent(side).Draw()


# hexagon
elif shape == 'h':
    side = innumber("Enter the side length of the hexagon: ")
    act = action()
    if act == 'a':
        print(f"The Area = {Hex(side).area()}")
    elif act == 'p':
        print(f"The Perimeter = {Hex(side).perimeter()}")
    else:
        Hex(side).Draw()


# octagon
elif shape == 'o':
    side = innumber("Enter the side length of the octagon: ")
    act = action()
    if act == 'a':
        print(f"The Area = {Oct(side).area()}")
    elif act == 'p':
        print(f"The Perimeter = {Oct(side).perimeter()}")
    else:
        Oct(side).Draw()