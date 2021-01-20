# -*- coding: utf-8 -*-

from itertools import combinations

def extractData(file_path):
    fp = open(file_path,'r')
    Lines = fp.readlines()
    for i in range(len(Lines)):
        Lines[i] = Lines[i].strip()
        
    firstLine = Lines[0]
    firstLArr = firstLine.split(' ')
    N = int(firstLArr[0])
    L = int(firstLArr[1])
    K = int(firstLArr[2])
    
    secondLine = Lines[1]
    Prods = secondLine.split(' ')
    
    Prefs = []
    for i in range(2,2+L):
        Line = Lines[i]
        Pi = Line.split(' ')
        Prefs.append(Pi)
    
    return N,L,K,Prods,Prefs

def getResult(Ai,Aj,Pref):
    N = len(Pref)
    for x in range(N):
        px = Pref[x]
        if px in Ai and px in Aj:
            return 0
        elif px in Ai:
            return 1
        elif px in Aj:
            return -1
        

def getScores(Ai,Aj,Prefs):
    
    pi = 0.0
    pj = 0.0
    
    L = len(Prefs)
    for x in range(L):
        res = getResult(Ai,Aj,Prefs[x])
        if res==1:
            pi = pi + 1.0
        elif res==0:
            pi = pi + 0.5
            pj = pj + 0.5
        elif res==-1:
            pj = pj + 1.0
            
    return pi,pj

def computeCopeland(PossAlliances, Prefs):
    numA = len(PossAlliances)
    points = [0.0 for i in range(numA)]
    isCondorcetWin = [True for i in range(numA)]
    for i in range(numA-1):
        for j in range(i+1,numA):
            ai = PossAlliances[i]
            aj = PossAlliances[j]
            pi, pj = getScores(ai,aj,Prefs)
            if pi>pj:
                points[i] = points[i] + 1.0
                isCondorcetWin[j] = False
            elif pi==pj:
                points[i] = points[i] + 0.5
                points[j] = points[j] + 0.5
            else:
                points[j] = points[j] + 1.0
                isCondorcetWin[i] = False
                
    return points, isCondorcetWin

FILE_PATH = './Data_2.txt'
N, L, K, RawProds, RawPrefs = extractData(FILE_PATH)

Prods = {}
for i in range(N):
    Prods[RawProds[i]] = i

Prefs = []
for i in range(L):
    Pref = []
    for j in range(N):
        Pref.append(Prods[RawPrefs[i][j]])
    Prefs.append(Pref)

print(N)
print(L)
print(K)
print(Prods)
print(Prefs)

prodInds = list(range(N))

PossAlliances = list(combinations(prodInds,K))
for i in range(len(PossAlliances)):
    PossAlliances[i] = list(PossAlliances[i])
print(PossAlliances)

points, isCondorcetWin = computeCopeland(PossAlliances,Prefs)
print(points)
print(isCondorcetWin)

CopelandWinner = []
IsCondorcetWinner = False

maxv = max(points)
for i in range(len(PossAlliances)):
    if points[i]==maxv:
        cp = []
        for j in range(K):
            cp.append(RawProds[PossAlliances[i][j]])
        CopelandWinner.append(cp)
        IsCondorcetWinner = isCondorcetWin[i]
        
print('The Copeland Winner Alliance for the given data is/are:')
for i in CopelandWinner:
    print(i)
    
print('Is/Are this/these Condorcet Winner/s?: ', IsCondorcetWinner)

