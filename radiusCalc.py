import math

def radiusCalc(radList):
	radius = []
	circumference = []
	na2 = []
	for i in radList:
		circumference.append(round((2*i*math.pi/0.246)/10, 0))
		na2.append(round((2*i*math.pi/0.246)/(10*math.sqrt(3)),0))
		radius.append(round(5*(0.246*circumference[-1]/math.pi),2))
	return circumference, na2, radius

def main():

	radList = [7.0, 8.2]
	n, na2, radius = radiusCalc(radList)
	for i in range(len(n)):
		print "radius: ", radius[i], "n= ", n[i], "na2= ", na2[i]
main()
