import sys
import random
import math
import numpy as np
from itertools import combinations
filename=input("Hey! This is a Baseline algorithm for counting triangles.\nPlease enter the file name of the file containing the edges. (eg. data/facebook_combined.txt ) \n\n")
with open(filename) as f:
    file = f.read().split('\n')
f.close()
edgeResDict={}
edgeResArray=[]
i=0
for line in file:
    if '#' in line or line=='':
        continue
    else:
        i+=1
        #print(i)
        u = line.split()[0]
        v = line.split()[1]
        #if (v,u) not in edgeResArray:
        edgeResArray.append((u, v))
        #if (v, u) in edgeResArray:
            #print (u,v)
        if u in edgeResDict:
            #if not (v in edgeResDict and u in edgeResDict[v]):
            edgeResDict[u].add(v)
            #if (v in edgeResDict and u in edgeResDict[v]):
               # print(u," ", v)
        else:
            edgeResDict[u] = set([v])
        if v in edgeResDict:
            edgeResDict[v].add(u)
        else:
            edgeResDict[v]=set([u])


#need to choose m' and m''
#Lower threshold as root n*2 and upper as n/2

mDashCount = random.randint(math.ceil(math.sqrt(len(edgeResArray))*2),math.ceil(len(edgeResArray)/2))
mDblDashCount = random.randint(math.ceil(math.sqrt(len(edgeResArray)) * 2), math.ceil(len(edgeResArray) / 2))
#chosing m' and m''
#mDash=[]
mDashDict = {}
mDblDash=[]
indices = np.random.choice(len(edgeResArray)-1, mDashCount, replace=False)
i=0
for index in indices:
    i += 1
    #print(i)
    edge=edgeResArray[index]
    u = edge[0]
    v = edge[1]
    if u in mDashDict:
        #check if the reverse of this edge is present, before adding
        mDashDict[u].add(v)
    else:
        # check if the reverse of this edge is present, before adding
        mDashDict[u] = set([v])
    if v in mDashDict:
        mDashDict[v].add(u)
    else:
        mDashDict[v] = set([u])
    #if (v,u) not in mDash:
     #   mDash.append(edge)
i=0
indices = np.random.choice(len(edgeResArray)-1, mDblDashCount, replace=False)
for index in indices:
    i += 1
    #print(i)
    mDblDash.append(edgeResArray[index])
mDashWedges={}
mDashClosed={}
i=0
for key in mDashDict:
    i += 1
    #print(i)
    curWedges=list(combinations(mDashDict[key], 2))
    for wedge in curWedges:
        if wedge[0] in mDashWedges:
            mDashWedges[wedge[0]].add(wedge)
        else:
            mDashWedges[wedge[0]]=set([wedge])
        if wedge[1] in mDashWedges:
            mDashWedges[wedge[1]].add(wedge)
        else:
            mDashWedges[wedge[1]]=set([wedge])
        mDashClosed[wedge]=0
i = 0
for edge in mDblDash:
    i+=1
    #print(i)
    if (edge[0] in mDashWedges and edge in mDashWedges[edge[0]]) or (edge[1] in mDashWedges and edge in mDashWedges[edge[1]]):
        #Triangle formed
        mDashClosed[edge]=1
pSmall=(list(mDashClosed.values()).count(1))/len(mDashClosed)
##################
i=0
totalWedges={}
totalClosed={}
for key in edgeResDict:
    i += 1
    #print(i)
    curWedges=list(combinations(edgeResDict[key], 2))
    for wedge in curWedges:
        if wedge[0] in totalWedges:
            totalWedges[wedge[0]].add(wedge)
        else:
            totalWedges[wedge[0]]=set([wedge])
        if wedge[1] in totalWedges:
            totalWedges[wedge[1]].add(wedge)
        else:
            totalWedges[wedge[1]]=set([wedge])
        totalClosed[wedge]=0
i=0
for edge in edgeResArray:
    i+=1
    #print(i)
    if (edge[0] in totalWedges and edge in totalWedges[edge[0]]) or (edge[1] in totalWedges and edge in totalWedges[edge[1]]):
        #Triangle formed
        totalClosed[edge]=1
pBig=(list(totalClosed.values()).count(1))/len(totalClosed)
actualNumberOfTriangles = list(totalClosed.values()).count(1)
estimatedNumberOfTriangles = pSmall*len(totalClosed)
print("Transitivity of sketch graph:",pSmall,"\n")
print("Transitivity of complete graph:",pBig,"\n")
#print("Actual Number of Triangles:",actualNumberOfTriangles,"\n","Estimated number of triangles:",estimatedNumberOfTriangles,"\n")









