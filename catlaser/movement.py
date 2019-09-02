import init_laser as laser

XPins = [3, 4, 17, 27]
YPins = [22, 10, 21, 20]


testlaser = laser.Laser(XPins, YPins, 0.005)

with open("test2.csv", "r") as smallcsv:
    for line in smallcsv:
        xy = line.strip().split(',')
        testlaser.MoveAbsolute(int(xy[0]), int(xy[1]))
testlaser.MoveAbsolute(0,0)
