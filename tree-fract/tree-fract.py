import math
import sys

from array import *

if len(sys.argv) < 2 :
	print ("Usage: " + sys.argv[0] + " file")
	exit (-1)

in_filename = sys.argv[1]
basename = 'tmpfile'

f = open(in_filename, 'r')
level = int(f.readline())
new_level = level + 1
print("At level " + str(level) )	
line = f.readline()

coords = line.split(' ')

if len(coords) < 2 :
	exit (1)

pt = coords[0].split(',')
tx = float(pt[0])
ty = float(pt[1])
print ("tx,ty=" + str(tx) + ", " + str(ty) )

pt = coords[len(coords)-1].split(',')



x_arr = array('f')
y_arr = array('f')

x_max = tx
y_max = ty
x_min = tx
y_min = ty


for coord in coords:
	print (coord)
	pts = coord.split(',')
	x=float(pts[0])
	y=float(pts[1])

	if x > x_max :
		x_max = x
	if x < x_min :
		x_min = x
	if y > y_max :
		y_max = y
	if y < y_min :
		y_min = y

	print ("x,y=" + str(x) + ", " + str(y) )
	print ("x|tx = " + str(x) + " | " + str(tx)  )
	print ("y|ty = " + str(y) + " | " + str(ty)  )
	print ("x`, y` = " + str(x-tx) + ", " + str(y-ty) )
	x_arr.append(x-tx)
	y_arr.append(y-ty)




if x_min == x_max :
	dx = 1.0
else :
	dx = x_max - x_min

if y_min == y_max :
	dy = 1.0
else :
	dy = y_max - y_min

#dx = x_max - x_min
dy = y_max - y_min
#full_scale = math.sqrt( dx*dx + dy*dy )
#dx = full_scale
dx = dy

print ("x_min,y_min=" + str(x_min) + ", " + str(y_min) )
print ("x_max,y_max=" + str(x_max) + ", " + str(y_max) )
print ("dx,dy=" + str(dx) + ", " + str(dy) )

ndx0=0
while ndx0 < len(x_arr) :
	x_arr[ndx0] = x_arr[ndx0]/dx
	y_arr[ndx0] = y_arr[ndx0]/dy
	print ("x``, y`` = " + str(x_arr[ndx0]) + ", " + str(y_arr[ndx0]) )
	ndx0 = ndx0 + 1


last_coord = coords[0]




#Translated:
# v = sqrt (x*x + y*y)
# w = x*y/v

ndx0=1

while ndx0 < len(coords) :
	f_outname = basename + "." + str(new_level) + "." + str(ndx0)
	f = open(f_outname, 'w')
	f.write( str(new_level) + '\n')
	f.write(last_coord)
	top_coord = coords[ndx0]
	print("SEGMENT " + str(ndx0) )
	print("last=" + last_coord)
	print("next=" + top_coord)
	pt = last_coord.split(',')
	x0 = float(pt[0])
	y0 = float(pt[1])

	pt = top_coord.split(',')
	x2 = float(pt[0])
	y2 = float(pt[1])
	print ("x2,y2=" + str(x2) + ", " + str(y2) )

	opp = y2 - y0
	adj = x2 - x0
	ang = - math.atan(opp/adj)
	print ("ang=" + str(ang) )

	centerX = x0
	centerY = y0
	scale = math.sqrt( opp*opp + adj*adj)
	print ("scale=" + str(scale) )

	ndx1=1
	while ndx1 < len(x_arr) :
		x = x_arr[ndx1]
		y = y_arr[ndx1]
		print ("x',y'=" + str(x*dx+tx) + ", " + str(y*dy+ty) )
		newX = x*math.cos(ang) - y*math.sin(ang);
		newY = x*math.sin(ang) + y*math.cos(ang);
		#newX = centerX + (x-centerX)*math.cos(ang) - (y-centerY)*math.sin(ang);
		#newY = centerY + (x-centerX)*math.sin(ang) + (y-centerY)*math.cos(ang);
		print ("newX,newY=" + str(newX) + ", " + str(newY) )

		print ("x',y'=" + str(newX*scale + x0) + ", " + str(newY*scale + y0) )
		f.write(" " + str(newX*scale + x0) + "," + str(newY*scale + y0))

		ndx1 = ndx1 + 1

	f.write("\n")
	f.close()
	last_coord=top_coord
	ndx0 = ndx0 + 1
