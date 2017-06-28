#!/usr/bin/python

nf = open('new.dat')
of = open('old.dat')

n_recid = []
o_recid = []
for line in nf:
    n_recid.append(int(line.split()[0]))
for line in of:
    o_recid.append(int(line.split()[0]))

print len(n_recid),len(o_recid)

for recid in n_recid:
    if recid not in o_recid:
        print 'recid in new but not old:',recid

