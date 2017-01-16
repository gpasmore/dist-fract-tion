# Python 2.7

import sys
import re
import xml.etree.ElementTree as ET

if len(sys.argv) != 2:
	print "Usage: " + sys.argv[0] + " svgfilepath"
	exit(1)

file = sys.argv[1]
print "Parsing: " + file

def decode_float(path):
	m = re.search('([-+]?[0-9]*\.?[0-9]+)(.*)', path)
	return  m.group(2),float(m.group(1))

def decode_point(path):
	point = []
	m = re.search('([-+]?[0-9]*\.?[0-9]+),([-+]?[0-9]*\.?[0-9]+)(.*)', path)
	point.append(float(m.group(1)))
	point.append(float(m.group(2)))
	print point
	return  m.group(3),point

def parse_path(path):
	print path
	count = 0
	points = []
	lines = []
	current_pt = [0.0,0.0]
	mode = 'M'
	relative = False
	while True:
		chr = path[:1]
		new_path = path[1:]
		print "chr='" + chr + "'"
		print "mode='" + mode + "'"
		print "relative: " + str(relative)
		if len(chr)<1:
			break
		if chr.isdigit() or chr=='-' or chr =='+':
			print 'mode: ' + mode
			if mode == 'M' or  mode == 'L':
				path,point = decode_point(path)
			if mode == 'H' or  mode == 'V':
				path,pt = decode_float(new_path)
				if mode == 'H':
					point = []
					point.append(pt)
					point.append(0.0)
				else:
					point = [0.0]
					point.append(pt)

			if relative:
				print "Add " + str(point) + " to " + str(current_pt)
				point[0] = point[0] + current_pt[0]
				point[1] = point[1] + current_pt[1]
				print "Got " + str(point)
			points.append(point)
			current_pt = point
			if relative:
				print "Rel to " + str(current_pt)
		elif chr == ' ':
			print 'Ignore Space'
			path = new_path
		elif chr == 'M' or chr == 'm':
			mode = 'M'
			relative = (chr == 'm')
			print 'Mode -> M'
			if len(points)>1:
				lines.append(points)
			points = []
			path = new_path
		elif chr == 'L' or chr == 'l':
			mode = 'L'
			print 'Mode -> L'
			relative = (chr == 'l')
			path = new_path
		elif chr == 'H' or chr == 'h':
			mode = 'H'
			print 'Mode -> H'
			relative = (chr == 'h')
			path = new_path
		elif chr == 'V' or chr == 'v':
			mode = 'V'
			print 'Mode -> V'
			relative = (chr == 'v')
			path = new_path
		else:
			print 'Unknown xform: ' + chr
			exit(0)
		count = count + 1
		if count > 30000:
			print 'Loop exceeded max iter'
			exit(0)
	if len(points)>1:
		lines.append(points)
	return lines

f = open(file, 'r')
svgstring = f.read()
print svgstring
svgstring = re.sub(' xmlns="[^"]+"', '', svgstring, count=1)

root = ET.fromstring(svgstring)
for path in root.iter('path'):
    lines = parse_path( path.get('d') )
    print "Path<" + path.get('id')  + ">: " + str(lines)
