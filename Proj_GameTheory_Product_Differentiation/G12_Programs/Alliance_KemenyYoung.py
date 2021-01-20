# -*- coding: utf-8 -*-

from itertools import combinations
from itertools import permutations

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
    pt = 0.0
    
    L = len(Prefs)
    for x in range(L):
        res = getResult(Ai,Aj,Prefs[x])
        if res==1:
            pi = pi + 1.0
        elif res==0:
            pt = pt + 1.0
        elif res==-1:
            pj = pj + 1.0
            
    return pi,pj,pt

def computeKYWin(PossAlliances, Prefs):
    numA = len(PossAlliances)
    tallyTab = [[0.0 for i in range(numA)] for j in range(numA)]
    for i in range(numA-1):
        for j in range(i+1,numA):
            ai = PossAlliances[i]
            aj = PossAlliances[j]
            pi,pj,pt = getScores(ai,aj,Prefs)
            tallyTab[i][j] = pi + 0.5*pt
            tallyTab[j][i] = pj + 0.5*pt

    arr = range(numA)
    perms = list(permutations(arr))
    for i in range(len(perms)):
        perms[i] = list(perms[i])

    maxs = 0
    KMWin = []
    checkWin = 0

    for i in range(len(perms)):
        sum = 0
        for x in range(numA-1):
            for y in range(x,numA):
                sum = sum + tallyTab[perms[i][x]][perms[i][y]]

        if sum>maxs:
            maxs = sum
            KMWin.clear()
            KMWin.append(PossAlliances[perms[i][0]])
            checkWin = perms[i][0]
        elif sum==maxs:
            KMWin.append(PossAlliances[perms[i][0]])
            checkWin = perms[i][0]

    isCondorcetWin = True
    for i in range(numA):
        if i!=checkWin:
            if tallyTab[checkWin][i]<tallyTab[i][checkWin]:
                isCondorcetWin = False

    return KMWin, isCondorcetWin



FILE_PATH = './Data_1.txt'
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

KMWin, isCondorcetWin = computeKYWin(PossAlliances,Prefs)

KMWinMobile = []

for temp in KMWin:
    Win = []
    for i in temp:
        Win.append(RawProds[i])
    KMWinMobile.append(Win)
        
print('The Kemeny Young Winner Alliance for the given data is/are:')
for i in KMWinMobile:
    print(i)
    
print('Is/Are this/these Condorcet Winner/s?: ', isCondorcetWin)

