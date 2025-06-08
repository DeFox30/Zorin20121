class Point:
    def __init__(self, x, y, color="black"):
        self.x = x
        self.y = y
        self.color = color

points = []
for i in range(1000):
    x = 1+2*i
    y = 1+2*i
    if i == 1:
        points.append(Point(x,y,"yellow"))
    else:
        points.append(Point(x,y))

# p1 = Point(10,20)
# p2 = Point(12,5,"red")
