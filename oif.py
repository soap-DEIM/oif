import sys
import re
import os.path

if len(sys.argv) == 2:
    if os.path.lexists(sys.argv[1]):
        print sys.argv[1]
        print sys.argv[1][:-4]
    else:
        print "Can't find file " + sys.argv[1]
        sys.exit()
else:
    print "Usage: python oif.py FILE_NAME.csv"
    sys.exit()

file_in = sys.argv[1]
file_out = file_in[:-4] + "_out.txt"
if '.csv' in file_in:
    f = open(file_in, 'r')
    out = open(file_out, 'w')
else:
    print "not a csv file"
    sys.exit()

fstdev = False
fcorr = False

stdev = []
corr = []

# format input
for line in f:
    
    if 'Basic' in line:
        fstdev = True
        continue
    if 'Covar' in line:
        fstdev = False
        continue
    if 'Ei' in line:
        fcorr = False
        continue
        
    if fstdev is True and 'Band' in line:
        line = re.sub('Band [0-9],', '', line)
        #print line
        stdev.append(line.split(',')[3])
    
    if 'Correlation' in line:
        fcorr = True
        fstdev = False
        continue
    if fcorr is True and 'Band' in line:
        line = re.sub('Band [0-9],', '', line)
        corr.append(line.split(','))

f.close()

# convert to float
bands = len(stdev)

for i in range(bands):
    stdev[i] = float(stdev[i])
    
for i in range(bands):
    for j in range(bands):
        corr[i][j] = abs(float(corr[i][j]))

print "stdev"
print stdev
print "\ncorr"
for i in corr:
    print i

# calculate oif
for i in range(bands):
    for j in range(i+1, bands):
        for k in range(j+1, bands):
            oif = (stdev[i]+stdev[j]+stdev[k]) / \
                  (corr[i][j]+corr[i][k]+corr[j][k])
            print str(i+1)+str(j+1)+str(k+1), '\t', round(oif, 6)
            out.write(str(i+1)+str(j+1)+str(k+1)+'\t'+'{:06f}'.format(round(oif, 6))+'\n')

out.close()    
