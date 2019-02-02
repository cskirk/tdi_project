import csv
import datetime
import time
import numpy
from scipy import stats

from matplotlib import pyplot
pyplot.rcParams.update({'font.size': 10})


store_data = []
filename = 'stores.csv'
with open(filename, 'rU') as csvfile:
    reader = csv.reader(csvfile)
    store_data = list(list(rec) for rec in csv.reader(csvfile, delimiter=','))

assist_data = []
filename = 'assistance.csv'
with open(filename, 'rU') as csvfile:
    reader = csv.reader(csvfile)
    assist_data = list(list(rec) for rec in csv.reader(csvfile, delimiter=','))


access_data = []
filename = 'access.csv'
with open(filename, 'rU') as csvfile:
    reader = csv.reader(csvfile)
    access_data = list(list(rec) for rec in csv.reader(csvfile, delimiter=','))

pop_data = []
filename = 'population.csv'
with open(filename, 'rU') as csvfile:
    reader = csv.reader(csvfile)
    pop_data = list(list(rec) for rec in csv.reader(csvfile, delimiter=','))

population_data = [[0,0,0,0,0,0]]

for i in range(1, len(pop_data)-1):
    new_list = []
    for j in range(3, 10):
        #print pop_data[i][j]
        if len(pop_data[i][j].split(',')) == 1:
            new_list.append(float(pop_data[i][j]))
        elif len(pop_data[i][j].split(',')) == 2:
            new_list.append(float(pop_data[i][j].split(',')[0] + pop_data[i][j].split(',')[1]))
        elif len(pop_data[i][j].split(',')) == 3:
            new_list.append(float(pop_data[i][j].split(',')[0] + pop_data[i][j].split(',')[1] + pop_data[i][j].split(',')[2]))
    population_data.append(new_list)

pop_2015 = []
pop_2010 = []
for i in range(1, len(population_data)):
    pop_2010.append(float(population_data[i][0]))
    pop_2015.append(float(population_data[i][5]))


rest_data = []
filename = 'restaurants.csv'
with open(filename, 'rU') as csvfile:
    reader = csv.reader(csvfile)
    rest_data = list(list(rec) for rec in csv.reader(csvfile, delimiter=','))


pch_access = []
pch_grocery = []
pch_super = []
pch_conv = []
pch_spec = []
pch_ff = []

data = {}
pop_la_2015 = []
pop_la_2010 = []
ff_2010 = []
fs_2010 = []
snap_2010 = []

state_dict = {}

for i in range(1, len(access_data)):
    if access_data[i][5] != '' and store_data[i][5] != '' and store_data[i][11] != '' and store_data[i][17] != '' and store_data[i][23] != '' and rest_data[i][5] != '' and assist_data[i][6] != '':
        if float(access_data[i][6]) > 0. and float(access_data[i][7]) > 0.:
            pch_access.append(float(access_data[i][5])/100.)
            pch_grocery.append(float(store_data[i][5])/100.)
            pch_super.append(float(store_data[i][11])/100.)
            pch_conv.append(float(store_data[i][17])/100.)
            pch_spec.append(float(store_data[i][23])/100.)
            pch_ff.append(float(rest_data[i][5])/100.)
            pop_la_2010.append(float(access_data[i][3]))
            pop_la_2015.append(float(access_data[i][4]))  
            ff_2010.append(float(rest_data[i][3]))
            fs_2010.append(float(rest_data[i][9]))
            snap_2010.append(float(assist_data[i][6]))
            if access_data[i][1] not in state_dict.keys():
                state_dict[access_data[i][1]] = float(access_data[i][4])
            if access_data[i][1] in state_dict.keys():
                state_dict[access_data[i][1]] += float(access_data[i][4])

print 1 - numpy.sum(pop_la_2015)/numpy.sum(pop_la_2010)
print 1 - numpy.sum(pop_2015)/numpy.sum(pop_2010)
print numpy.sum(pop_la_2015)/numpy.sum(pop_2015)

# plot fractional change in low access population from 2010 to 2015
fig = pyplot.figure(figsize=(7,6))
ax = fig.add_subplot(111)

ax.plot(pop_la_2015, 'ko', label='fractional change in low access population')

ax.legend(loc='upper left', shadow = True, fontsize=10)
#ax.set_xlim([-10, 10])
#ax.set_ylim([-2, 10])
ax.set_ylabel('population with low access to stores in 2015', fontsize=15, fontname='serif')
ax.set_xlabel('county', fontsize=15, fontname='serif')
ax.set_xticklabels([])


fig.tight_layout()
fig.savefig('frac_change_la.png')


fig = pyplot.figure(figsize=(7,6))
ax = fig.add_subplot(111)

ax.plot(pch_access, pch_grocery, 'bo', label='grocery')
#ax.plot(pch_access, pch_conv, 'ro', label='convenience')
#ax.plot(pch_access, pch_spec, 'go', label='specialty')
#ax.plot(pch_access, pch_spec, 'mo', label='supercenter')

#ax.legend(loc='lower left', shadow = True, fontsize=10)
ax.set_xlim([-2, 10])
#ax.set_ylim([0, 1.2])
ax.set_xlabel('fractional change in low access population', fontsize=15)
ax.set_ylabel('change in number of stores', fontsize=15)

fig.tight_layout()
fig.savefig('out.png')


fig = pyplot.figure(figsize=(7,6))
ax = fig.add_subplot(111)

a1, b1 = numpy.polyfit(pop_la_2010, pch_grocery, 1)
a2, b2 = numpy.polyfit(ff_2010, pch_grocery, 1)
a3, b3 = numpy.polyfit(ff_2010, pch_grocery, 1)


ax.plot(pop_la_2010, pch_grocery, 'ko', label='grocery v. fast food')
#ax.plot(pch_access, pch_conv, 'ro', label='convenience')
#ax.plot(pch_access, pch_spec, 'go', label='specialty')
#ax.plot(pch_access, pch_spec, 'mo', label='supercenter')

#ax.legend(loc='lower left', shadow = True, fontsize=10)
#ax.set_xlim([-1, 2])
#ax.set_ylim([0, 1.2])
ax.set_xlabel('population with low access to stores', fontsize=15)
ax.set_ylabel('grocery stores increased from 2010 to 2015', fontsize=15)

fig.tight_layout()
fig.savefig('out.png')


fig = pyplot.figure(figsize=(12,6))
ax = fig.add_subplot(111)

c = 0
labels = []
ticks = []
for key in state_dict.keys():
    print key
    ax.plot([c, c], [0, state_dict[key]/10000], 'r-', linewidth = 10)
    ticks.append(c)
    c += 1
    labels.append(key)
    

#ax.legend(loc='lower left', shadow = True, fontsize=10)
#ax.set_xlim([-1, 2])
ax.set_ylim([0, 600])
ax.set_xlabel('state', fontsize=15, fontname='serif')
ax.set_ylabel('10,000 people with low access to stores', fontsize=15, fontname='serif')
ax.set_xticks(ticks)
ax.set_xticklabels(labels)

fig.tight_layout()
fig.savefig('out.png')

