import re
import sys

if len(sys.argv) < 2 :
	print ("Usage: " + sys.argv[0] + " file")
	exit (-1)

filebase = sys.argv[1]
inputfile = filebase + ".svg"
outputfile = filebase + ".temp"

if len(sys.argv) < 2 :
	print ("Usage: " + sys.argv[0] + " file")
	exit (-1)


pat = re.compile('polyline\s+points\s*=\s*"([^"]+)"', re.IGNORECASE)
#pat = re.compile('polyline', re.IGNORECASE)
f_in = open(inputfile, 'r')
f_out = open(outputfile, 'w')
f_out.write('0\n')
for line in f_in:
	print("Checking " + line)
	m = pat.search(line)
	if m :
	 	print ("Matched " + m.group())
	 	f_out.write(m.group(1))

