import init_laser as laser

XPins = [12, 25, 24, 23]
YPins = [4, 17, 27, 22]
Laser_Pin = 16

testlaser = laser.Laser(XPins, YPins, Laser_Pin, 0.005)

testlaser.Laser_On()
testlaser.Laser_Off()



"""
with open("test.csv", "r") as smallcsv:
    for line in smallcsv:
        xy = line.strip().split(',')
        testlaser.MoveAbsolute(int(xy[0]), int(xy[1]))
testlaser.Laser_Off()
testlaser.MoveAbsolute(0,0)
"""