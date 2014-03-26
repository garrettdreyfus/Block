import os
import sys

if len(sys.argv) < 2:
    sys.stderr.write('Usage: sys.argv[0] ')
    sys.exit(1)
    
with file(sys.argv[1]) as f:
    s = f.read()
    lines = s.split('\r')
    for l in lines:
        # print "LINE: starting with:", l[0:8], " has the following structure:"
        fields = l.split('\t')
        if len(fields) == 5:
            for i in range(len(fields)):
                fields[i] = fields[i].decode('utf-8', 'ignore')
            fields[3] = fields[3].replace('\"', "")
            for f in fields:
                print f, "\t",
            print "\r"
        else:
            sys.stderr.write("ERROR: line: " + l + "\n")
