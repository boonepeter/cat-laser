import init_laser as laser

XPins = [2, 3, 4, 17]
YPins = [10, 9, 11, 5]

testlaser = laser.Laser(XPins, YPins)

with open("test.csv", "r") as smallcsv:
    for line in smallcsv:
        xy = line.strip().split(',')
        testlaser.MoveAbsolute(int(xy[0]), int(xy[1]))