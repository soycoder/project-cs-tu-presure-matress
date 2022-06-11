_range = "x1x5-y2y5"

x = _range.split("-")[0]
y = _range.split("-")[1]
# x - axis
x1 = int(x.split("x")[1])
x2 = int(x.split("x")[2])
# y - axis
y1 = int(y.split("y")[1])
y2 = int(y.split("y")[2])

for xi in range(x1,x2+1):
    for yi in range(y1,y2+1):
        print(xi ,yi)