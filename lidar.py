'''
Code written by Joe Squillace 
'''

from laspy.file import File
from scipy.spatial import Delaunay
import numpy as np
import matplotlib.pyplot as plt

global values

'''
Open file and store header and point records
'''
inFile = File('/Users/joesquillace/workspace/lidar/nz/small_nz.las', mode='r')

header = inFile.header
point_records = inFile.points

'''
Create new record of final return (ground) points for DTM
'''
num_returns = inFile.num_returns
return_num = inFile.return_num
ground_points = inFile.points[num_returns == return_num]

print("%i points out of %i were last return (ground) points" % 
	(len(ground_points), len(inFile)))

'''
Display number of returns for each pulse
Display histogram of all returns
'''
one_returns = inFile.points[num_returns == 1]
two_returns = inFile.points[num_returns == 2]
three_returns = inFile.points[num_returns == 3]
four_returns = inFile.points[num_returns == 4]

print ("%i points are part of a pulse with 1 returns" % len(one_returns))
print ("%i points are part of a pulse with 2 returns" % len(two_returns))
print ("%i points are part of a pulse with 3 returns" % len(three_returns))
print ("%i points are part of a pulse with 4 returns" % len(four_returns))

plt.hist(inFile.num_returns)
plt.title("Histogram of Returns (%i Total)" % len(num_returns))
plt.show()

'''
Display return numbers
'''
surface_points = inFile.points[return_num == 1]

print("%i points out of %i were first return (surface) points" % 
	(len(surface_points), len(inFile)))

first = inFile.points[return_num == 1]
second = inFile.points[return_num == 2]
third = inFile.points[return_num == 3]
fourth = inFile.points[return_num == 4]

print ("%i points were first returns" % len(first))
print ("%i points were second returns" % len(second))
print ("%i points were third returns" % len(third))
print ("%i points were fourth returns" % len(fourth))

plt.hist(inFile.return_num)
plt.title("Histogram of Returns (%i Total)" % len(return_num))
plt.show()


'''
Conduct Delaunay triangulation to form TIN graph of ground points
'''

INT_PERCENT_OF_POINTS_TO_INCLUDE = 10
values = []

for i in range (0, len(ground_points), (100/INT_PERCENT_OF_POINTS_TO_INCLUDE)):
	
	x_val = ground_points[i][0][0]
	y_val = ground_points[i][0][1]
	coord = [x_val, y_val]
	values.append(coord)

points = np.array(values)
points -= points.mean(axis=0)
tri = Delaunay(points)

'''
Display generated TIN of ground points
For better visualization, only plot simplices
'''

plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
plt.plot(points[:,0], points[:,1], 'o')
plt.show()
