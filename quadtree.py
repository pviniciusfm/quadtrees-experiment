import random
from p5 import *

class Point:
    def __init__(self, lat, long):
        self.x = lat
        self.y = long

    def render(self):
        stroke(255)
        stroke_weight(2)
        point(self.x, self.y)

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def within_bounds(self, point):
        result = (point.x > self.x and point.x < self.x + self.w) and (point.y> self.y and point.y < self.y + self.h)
        if not result:
            print(f'not wihin bounds point.x = {point.x}, point.y = {point.y}, self.x = {self.x}, self.w = {self.w}, self.y = {self.y}. self.h = {self.h}')
        return result

class QuadTree:
    def __init__(self, boundary, capacity):
        self.capacity = capacity
        self.boundary = boundary
        self.points = set()
        self.divided = False

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        top_left_bound = Rectangle(x, y, w/2, h/2)
        self.top_left = QuadTree(top_left_bound, self.capacity)
        top_right_bound = Rectangle(x + w/2, y, w/2, h/2)
        self.top_right = QuadTree(top_right_bound, self.capacity)

        bottom_left_bound = Rectangle(x, y + h/2, w/2, h/2)
        self.bottom_left = QuadTree(bottom_left_bound, self.capacity)
        bottom_right_bound = Rectangle(x + w/2, y + h/2, w/2, h/2)
        self.bottom_right = QuadTree(bottom_right_bound, self.capacity)

        self.divided = True

    def insert(self, point):
        if not self.boundary.within_bounds(point):
            return

        if self.divided:
            self.top_left.insert(point)
            self.top_right.insert(point)
            self.bottom_left.insert(point)
            self.bottom_right.insert(point)
        else:
          if len(self.points) < self.capacity:
            self.points.add(point)
          else:
            print(f"at capacity -> {len(self.points)} points. Dividing...")
            self.subdivide()
            self.insert(point)

    def render(self):
        stroke(255)
        no_fill()

        rect(self.boundary.x, self.boundary.y, self.boundary.w, self.boundary.h)

        for p in self.points:
            p.render()

        if self.divided:
            self.top_left.render()
            self.top_right.render()
            self.bottom_left.render()
            self.bottom_right.render()

def setup():
    size(600, 600)
    background(255)
    fill(126)
    qtree.render()

def key_pressed():
    background(24)

def draw():
    background(0)

    if mouse_is_pressed:
        stroke(255)
        print(mouse_x, mouse_y)
        qtree.insert(Point(mouse_x, mouse_y))
    else:
        stroke(100)

    background(0)
    qtree.render()

if __name__=="__main__":
    global qtree
    boundary = Rectangle(0, 0, 1200, 1200)
    qtree = QuadTree(boundary, 4)
    run()

