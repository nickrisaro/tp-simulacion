import matplotlib.pyplot as plt
import random
import turtle

turtle.speed('slowest')

def randomWalk(length):
    x,y = 0,0
    posicionX,posicionY = [x],[y]

    for i in range(length):
        siguientePaso = random.randint(1,4)
        if siguientePaso == 1:
            x += 1
        elif siguientePaso == 2:
            y += 1
        elif siguientePaso ==3 :
            x += -1
        else :
            y += -1
        posicionX.append(x)
        posicionY.append(y)
    return [posicionX,posicionY]


walk = randomWalk(1000)

for x, y in zip(*walk):
    turtle.goto(x*10,y*10)

turtle.exitonclick()
