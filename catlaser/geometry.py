import math

height = 10

def ReturnAngles(X, Y):
    hypot = math.sqrt((X*X) + (Y*Y))
    if X == 0:
        degX = 0
    else:
        degX = math.degrees(math.atan(X / Y))
    if Y <= 0:
        degY = 0
    else:
        degY = math.degrees(math.atan(hypot / height))
    return degX, degY

def CalcSteps(X, Y, curDegX, curDegY):
    newDegX, newDegY = ReturnAngles(X, Y)
    difX = newDegX - curDegX
    difY = newDegY - curDegY
    stepsX = (difX * 2038) / 360
    stepsY = (difY * 2038) / 360
    return stepsX, stepsY

print(ReturnAngles(10, 15))
print(ReturnAngles(-10, 10))
print(ReturnAngles(-5, 5))
print(ReturnAngles(0,0))
print(ReturnAngles(0, 10))

curX = 45
curY = 45
X = 5
Y = 5
print("Start")

for i in range(5):
    curX, curY = ReturnAngles(X, Y)
    print(curX, curY)
    Y += 1
    X += 1

    print(CalcSteps(X, Y, curX, curY))



