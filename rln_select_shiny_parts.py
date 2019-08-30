#!/usr/bin/env python

# get thet particles from a shiny file.

import sys

###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile_new(f):
    inhead = True
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    count = 0
    labcount = 0
    for i in alldata:
        if '_rln' in i:
            labelsdic[i.split()[0]] = labcount
            labcount +=1
        if inhead == True:
            header.append(i.strip("\n"))
            if '_rln' in i and '#' in i and  '_rln' not in alldata[count+1] and '#' not in alldata[count+1]:
                inhead = False
        elif len(i.split())>=1:
            data.append(i.split())
        count +=1
    
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#

try:
    (labels,header,data) = read_starfile_new(sys.argv[1])
    (shiny_labels,shiny_header,shiny_data) = read_starfile_new(sys.argv[2])
except:
    sys.exit('\nUSAGE: rln_select_shiny_parts.py <selected parts star file> <shiny star file>')


selIDs = {}
for particle in data:
    x = particle[labels['_rlnCoordinateX']]
    y = particle[labels['_rlnCoordinateY']]
    micrograph = particle[labels['_rlnMicrographName']]
    selIDs['{}{}{}'.format(x,y,micrograph)] = particle[labels['_rlnImageName']]



output = open('selected_particles.star','w')
for i in shiny_header:
    output.write('{0}\n'.format(i))
    
n= 0
for i in shiny_data:
    x = i[labels['_rlnCoordinateX']]
    y = i[labels['_rlnCoordinateY']]
    micrograph =i[labels['_rlnMicrographName']]
    ID = '{}{}{}'.format(x,y,micrograph)
    if ID in selIDs:
        output.write('{0}\n'.format('   '.join(i)))
        print('{0} <-- {1}'.format(i[labels['_rlnImageName']],selIDs[ID]))
        n+=1

print('{0} shiny particles').format(len(shiny_data))
print('{0} selected particles').format(len(selIDs))
print('{0}/{1} particles found'.format(n,len(selIDs)))