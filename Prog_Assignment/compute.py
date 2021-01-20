# DO NOT CHANGE THE NAME OF THIS SCRIPT

import numpy as np
# DO NOT IMPORT ANY GAME THEORY RELATED PACKAGES

# DO NOT CHANGE THE NAME OF ANY METHOD OR ITS INPUT OUTPUT BEHAVIOR
# INPUT CONVENTION
# file_name: Name of the game file either in .efg or .nfg depending on the fuction

#QUESTION 1
def computeSDS( file_name ):
    # Read the game from the input file
    nfg = NFGGame()
    tabRep, players, strategies = nfg.readNFGGame(file_name)
    
    sdso = NFGCalc()
    SDSlist = []
    for i in range(players):
        SDSlist = sdso.getSDS(SDSlist,i,tabRep,players,strategies)
    
    #print(SDSlist)
    return SDSlist
    
    # Make sure you are returning a list as specified in the assignment

#QUESTION 2
def computeWDS( file_name ):
    nfg = NFGGame()
    tabRep, players, strategies = nfg.readNFGGame(file_name)
    #print(tabRep, players, strategies)
    # Read the game from the input file
    wdso = NFGCalc()
    WDSlist = []
    for i in range(players):
        WDSlist = wdso.getWDS(WDSlist,i,tabRep,players,strategies)
    
    #print(WDSlist)
    return WDSlist
    # Make sure you are returning a list as specified in the assignment

#QUESTION 3
def computePSNE( file_name ):
    # Read the game from the input file
    nfg = NFGGame()
    tabRep, players, strategies = nfg.readNFGGame(file_name)
    psno = NFGCalc()
    maxstrmat = psno.getMaxPlayerStratComb(players,tabRep,strategies)
    psneVals = psno.getPsneVals(maxstrmat,players,strategies,tabRep)
    #print(psneVals)
    return psneVals
    
    # Make sure you are returning a list of list as specified in the assignment

#QUESTION 4
def efg_NFG( file_name ):
    # Read the game from the input file
    efg = EFGGame()
    gameTitle, numplayer, players, treeNode = efg.readEFGGame(file_name)
            
    NFGLines = []
    Line = 'NFG 1 R ' + gameTitle
    NFGLines.append(Line)
    
    efgOb = EFGCalc()
    infoSet = efgOb.getInfoSetMap(treeNode, numplayer)
    infActionMapping = efgOb.getActionsForInfoSet(numplayer,players,treeNode,infoSet)
    
    Line = '{ '
    for pl in players:
        Line = Line + pl + ' '
    Line = Line + '} { '
    numstrat = [0]
    numutilities = 1
    for i in range(1,numplayer+1):
        numst=1
        for j in range(1,infoSet[i]+1):
            numst = numst*len(infActionMapping[i][j])
        numstrat.append(numst)
        numutilities = numutilities*numst
        Line = Line + str(numst) + ' '
    Line = Line + '}' 
    NFGLines.append(Line)
    
    currstate = [[1 for j in range(infoSet[i]+1)] for i in range(numplayer+1)]

    Line = ' '
    for i in range(numutilities):
        utilityvals = efgOb.getUtilities(currstate,numplayer,treeNode)
        for j in utilityvals:
            Line = Line + str(int(j)) + ' '
        #print(currstate, ' for ' ,utilityvals)
        currstate = efgOb.updateCurrState(currstate,numplayer,infoSet,infActionMapping)

    Line = Line.strip()
    NFGLines.append(Line)    
    #print(NFGLines)
    return NFGLines
    
    
    # Make sure you are returning a list of strings as specified in the assignment

#QUESTION 5
def computeSPNE( file_name ):
    # Read the game from the input file
    efg = EFGGame()
    gameTitle, numplayer, players, treeNode = efg.readEFGGame(file_name)
    
    efgOb = EFGCalc()
    spnestr, utilities = efgOb.getSPNE(treeNode,numplayer)
    #print(spnestr)
    return spnestr
    
    # Make sure you are returning a list as specified in the assignment
    
class NFGGame:

    def readNFGGame(self,file_name):
        file1 = open(file_name, 'r') 
        Lines = file1.readlines()
        for i in range(len(Lines)):
            Lines[i] = Lines[i].strip()
        currLine=0
        currpos=0
        currpos, currLine, token = self.getToken(currLine,currpos,Lines) #NFG
        if(token != "NFG"):
            return
        currpos, currLine, token = self.getToken(currLine,currpos,Lines) #1
        currpos, currLine, token = self.getToken(currLine,currpos,Lines) #R
        
        currpos, currLine, strLit = self.getStringLiteral(currLine,currpos,Lines) #Game Name
        #print(strLit, currpos, currLine)
        gameTitle = strLit

        currpos, currLine, token = self.getToken(currLine,currpos,Lines) # '{'

        numplayer = 0
        players = []
        
        while(self.checkStringLiteralPresent(currLine,currpos,Lines)):
            currpos, currLine, strLit = self.getStringLiteral(currLine,currpos,Lines)
            numplayer = numplayer + 1
            players.append(strLit)
            
        #print(players)
            
        currpos, currLine, token = self.getToken(currLine,currpos,Lines) # '}'
        currpos, currLine, token = self.getToken(currLine,currpos,Lines) # '{'
        
        numstr = []
        
        for i in range(numplayer):
            currpos, currLine, token = self.getToken(currLine,currpos,Lines)
            numstr.append(int(token))
        
        currpos, currLine, token = self.getToken(currLine,currpos,Lines) # '}'
        
        #print(numstr)
        utilityshape = []
        numutilities = 1
        for x in numstr:
            utilityshape.append(x)
            numutilities = numutilities*x
        utilityshape.append(numplayer)
        utilityshape = tuple(utilityshape)
        utilities = np.zeros(shape=utilityshape)
        #print(utilityshape)
        
        indnumpl = np.zeros(shape=(numplayer))
        for i in range(numutilities):
            temp = np.zeros(numplayer)
            for j in range(numplayer):
                currpos, currLine, token = self.getToken(currLine,currpos,Lines)
                temp[j] = float(token)
            utilities = self.setUtilityVal(utilities,numplayer,indnumpl,0,temp)
            indnumpl = self.getNextSequence(indnumpl,numstr)
            
        #print(utilities)

        return utilities,numplayer,numstr
        
    def getNextSequence(self,indnumpl,numstr):
        l = len(indnumpl)
        for i in range(l):
            if(indnumpl[i]!=(numstr[i]-1)):
                indnumpl[i] = indnumpl[i]+1
                for j in range (i):
                    indnumpl[j]=0
                break
        return indnumpl
        
    def setUtilityVal(self,utilities,numplayer,indnumpl,ind,temp):
        
        if ind==numplayer:
            utilities = temp
            return utilities
        
        z = utilities[int(indnumpl[ind])]
        z = self.setUtilityVal(z,numplayer,indnumpl,ind+1,temp)
        utilities[int(indnumpl[ind])] = z
        return utilities
        
        
    def checkStringLiteralPresent(self,currLine,currPos,Lines):
        line = Lines[currLine]
        lineSize = len(line)
        flag = True
        separators = [' ','\t','\r']
        while flag==True:
            while currPos<lineSize and line[currPos] in separators:
                currPos=currPos+1
            if currPos == lineSize:
                currPos = 0
                currLine=currLine+1
                if currLine==len(Lines):
                    flag=False
                    break
                line = Lines[currLine]
                lineSize = len(line)
            else:
                if(line[currPos]=='"'):
                    return True
                return False
        return False
    
    def getStringLiteral(self,currLine,currPos,Lines):
        strLit = ''
        line = Lines[currLine]
        lineSize = len(line)
        flag = True
        separators = [' ','\t','\r']
        while flag==True:
            while currPos<lineSize and line[currPos] in separators:
                currPos=currPos+1
            if currPos == lineSize:
                currPos = 0
                currLine=currLine+1
                if currLine==len(Lines):
                    flag=False
                    break
                line = Lines[currLine]
                lineSize = len(line)
            else:
                strLit+=line[currPos]
                currPos=currPos+1
                while currPos<lineSize and (line[currPos]!='"' or line[currPos-1]=='\\'):
                    strLit = strLit + line[currPos]
                    currPos = currPos+1
                strLit+=line[currPos]
                currPos = currPos + 1
                flag=False
                if currPos == lineSize:
                    currPos = 0
                    currLine=currLine+1
                    if currLine==len(Lines):
                        break
                    line = Lines[currLine]
                    lineSize = len(line)
        return currPos, currLine, strLit
                    
        
    def getToken(self,currLine,currPos,Lines):
        token = ''
        line = Lines[currLine]
        lineSize = len(line)
        flag = True
        separators = [' ','\t','\r']
        while flag==True:
            while currPos<lineSize and line[currPos] in separators:
                currPos=currPos+1
            if currPos == lineSize:
                currPos = 0
                currLine=currLine+1
                if currLine==len(Lines):
                    flag=False
                    break
                line = Lines[currLine]
                lineSize = len(line)
            else:
                while currPos< lineSize and line[currPos] not in separators:
                    token = token + line[currPos]
                    currPos = currPos+1
                flag=False
                if currPos == lineSize:
                    currPos = 0
                    currLine=currLine+1
                    if currLine==len(Lines):
                        break
                    line = Lines[currLine]
                    lineSize = len(line)
                    
        return currPos, currLine, token
    
class NFGCalc:
    
    def getWDS(self,WDSlist,player,tabRep,nump,numst):
        
        found = False
        for i in range(numst[player]):
            if found==True:
                WDSlist.append(0)
            else:
                strati = self.getStrat(i,player,tabRep,nump,numst)
                bfl = True
                for j in range(numst[player]):
                    if j!=i:
                        stratj = self.getStrat(j,player,tabRep,nump,numst)
                        valid = self.checkIWDomJ(strati,stratj)
                        #print(strati, stratj, i, j)
                        if valid==False:
                            bfl=False
                            break
                
                if bfl==True:
                    WDSlist.append(1)
                    found=True
                else:
                    WDSlist.append(0)
        
        #print(WDSlist)
        return WDSlist
    
    def getSDS(self,SDSlist,player,tabRep,nump,numst):
        found = False
        for i in range(numst[player]):
            if found==True:
                SDSlist.append(0)
            else:
                strati = self.getStrat(i,player,tabRep,nump,numst)
                bfl = True
                for j in range(numst[player]):
                    if j!=i:
                        stratj = self.getStrat(j,player,tabRep,nump,numst)
                        valid = self.checkISDomJ(strati,stratj)
                        #print(strati, stratj, i, j)
                        if valid==False:
                            bfl=False
                            break
                
                if bfl==True:
                    SDSlist.append(1)
                    found=True
                else:
                    SDSlist.append(0)
        
        #print(WDSlist)
        return SDSlist
    
    def getMaxPlayerStratComb(self,players,tabRep,strats):
        
        maxshap = []
        numutilities = 1
        for i in range(len(strats)):
            numutilities = numutilities * strats[i]
            maxshap.append(strats[i] + 1)
        maxshap = tuple(maxshap)
        maxmatr = np.zeros(shape=maxshap)
        
        for i in range(players):
            numiter = int(numutilities/(strats[i]))
            indnumpl = [0 for i in range(players)]
            for j in range(numiter):
                maxv = self.setMaxValUtil(i,indnumpl,players,strats,tabRep,maxmatr)
                maxmatr = self.setToMaxMatr(i,indnumpl,players,strats,maxmatr,maxv,0)
                for k in range(players):
                    if (k!=i) and (indnumpl[k]!=(strats[k]-1)):
                        indnumpl[k] = indnumpl[k]+1
                        for l in range(k):
                            if l!=i:
                                indnumpl[l]=0
                        break
                
        return maxmatr

    def setToMaxMatr(self,pln,indnumpl,numpl,numstrat,maxmatr,maxv,ind):
        
        if ind==numpl:
            return maxv
        
        if(ind==pln):
            maxmatr[int(numstrat[pln])] = self.setToMaxMatr(pln,indnumpl,numpl,numstrat,maxmatr[int(numstrat[pln])],maxv,ind+1)
        else:
            maxmatr[indnumpl[ind]] = self.setToMaxMatr(pln,indnumpl,numpl,numstrat,maxmatr[indnumpl[ind]],maxv,ind+1)
            
        return maxmatr

    def setMaxValUtil(self,pln,indnumpl,numpl,numstr,tabRep,maxmatr):
        values = []
        for i in range(numstr[pln]):
            indnumpl[pln]=i
            uv = self.getUtilityValue(pln,tabRep,numpl,numstr,indnumpl,0)
            values.append(uv)
        return max(values)
            
        
    def getPsneVals(self,maxstrmat,numpl,strategies,tabRep):
        psneVals = []
        indnumpl = np.zeros(shape=(numpl))
        numutilities=1
        for i in range(len(strategies)):
            numutilities = numutilities*strategies[i]
            
        for i in range(numutilities):
            stratVals = self.getAllStratsForComb(indnumpl,tabRep,numpl,strategies,0)
            isPsne = self.checkForPsne(indnumpl,stratVals,maxstrmat,numpl,strategies)
            if isPsne:
                coordList = []
                for x in indnumpl:
                    coordList.append(int(x))
                psneVals.append(coordList)
            siz = len(indnumpl)
            for j in range(siz):
                if(indnumpl[j]!=(strategies[j]-1)):
                    indnumpl[j] = indnumpl[j]+1
                    for k in range(j):
                        indnumpl[k]=0
                    break
            
        return psneVals
    
    def checkForPsne(self,indnumpl,stratVals,maxstrmat,numpl,numstr):
        for i in range(numpl):
            strVal = stratVals[i]
            maxv = self.getFromMaxMatr(indnumpl,i,maxstrmat,numpl,numstr,0)
            if strVal!=maxv:
                return False
        return True
    
    def getFromMaxMatr(self,indnumpl,pln,maxmatr,numpl,numstr,ind):
        if ind==numpl:
            return maxmatr
        
        if ind==pln:
            return self.getFromMaxMatr(indnumpl,pln,maxmatr[int(numstr[pln])],numpl,numstr,ind+1)
        else:
            return self.getFromMaxMatr(indnumpl,pln,maxmatr[int(indnumpl[ind])],numpl,numstr,ind+1)

    def getAllStratsForComb(self,indnumpl,tabRep,numpl,strategies,ind):
        
        if ind==numpl:
            return tabRep
        
        subTab = tabRep[int(indnumpl[ind])]
        return self.getAllStratsForComb(indnumpl,subTab,numpl,strategies,ind+1)
        
    
    def checkISDomJ(self,strati,stratj):
        siz = len(strati)
        flag = True
        for i in range(siz):
            if strati[i]<=stratj[i]:
                return False
        return flag    
    
    def checkIWDomJ(self,strati,stratj):
        siz = len(strati)
        flag = False
        for i in range(siz):
            if strati[i]>=stratj[i]:
                if strati[i]>stratj[i]:
                    flag = True
            else:
                return False
        return flag
    
    def getStrat(self,stnum,plnum,tabRep,nump,numst):
        
        stValues = []
        indnumpl = np.zeros(shape=(nump))
        indnumpl[plnum] = stnum
        
        numutilities = 1
        for i in range(len(numst)):
            if i != plnum:
                numutilities = numutilities*numst[i]
                
        for i in range(numutilities):
            uv = self.getUtilityValue(plnum,tabRep,nump,numst,indnumpl,0)
            stValues.append(uv)
            indnumpl = self.updateIndNumPl(indnumpl,plnum,nump,numst)
        return stValues
            
        
    def getUtilityValue(self,plnum,tabRep,nump,numst,indnumpl,ind):
        
        if ind==nump:
            return tabRep[plnum]
        
        matr = tabRep[int(indnumpl[ind])]
        return self.getUtilityValue(plnum,matr,nump,numst,indnumpl,ind+1)
    
    def updateIndNumPl(self,indnumpl,plnum,nump,numst):
        
        for i in range(nump):
            if(i!=plnum):
                if(indnumpl[i]!=(numst[i]-1)):
                    indnumpl[i] = indnumpl[i]+1
                    for j in range(i):
                        if(j!=plnum):
                            indnumpl[j]=0
                    break
        return indnumpl
    
class EFGGame:
    
    def readEFGGame(self,file_name):
        file1 = open(file_name, 'r') 
        Lines = file1.readlines()
        for i in range(len(Lines)):
            Lines[i] = Lines[i].strip()
        currLine=0
        currpos=0
        
        currpos, currLine, token = self.getToken(currLine,currpos,Lines) #EFG
        currpos, currLine, token = self.getToken(currLine,currpos,Lines) #2
        currpos, currLine, token = self.getToken(currLine,currpos,Lines) #R
        
        currpos, currLine, strLit = self.getStringLiteral(currLine,currpos,Lines) #Game Name
        #print(strLit, currpos, currLine)
        gameTitle = strLit
        #print(gameTitle)
        
        currpos, currLine, token = self.getToken(currLine,currpos,Lines) # '{'
        numplayer = 0
        players = []
        
        while(self.checkStringLiteralPresent(currLine,currpos,Lines)):
            currpos, currLine, strLit = self.getStringLiteral(currLine,currpos,Lines)
            numplayer = numplayer + 1
            players.append(strLit)
            
        #print(players)
        
        currpos, currLine, token = self.getToken(currLine,currpos,Lines) # '}'        
        
        if self.checkStringLiteralPresent(currLine,currpos,Lines):
            currpos, currLine, token = self.getStringLiteral(currLine,currpos,Lines) #""
        
        treeNode = TreeNode()
        currpos,currLine, treeNode = self.recursCreateTree(currpos,currLine,Lines,treeNode)                
        return gameTitle, numplayer, players, treeNode
    
    def recursCreateTree(self,currpos,currLine,Lines,trNode):
        currpos, currLine, trNode = self.createTreeNode(currpos, currLine, Lines, trNode)
        if trNode.type=='p':
            acts = trNode.action
            for i in range(len(acts)):
                tempNode = TreeNode()
                trNode.child.append(tempNode)
                tempNode.par = trNode
                currpos,currLine,tempNode = self.recursCreateTree(currpos,currLine,Lines,tempNode)
                
        return currpos, currLine, trNode
        
    def createTreeNode(self, currpos, currLine, Lines, treeNode):
        
        currpos,currLine, nodetyp = self.getToken(currLine,currpos, Lines)
        treeNode.type = nodetyp
        
        if(nodetyp=='p'):
            currpos, currLine, nodeName = self.getStringLiteral(currLine,currpos,Lines)
            treeNode.nodeName = nodeName
            currpos, currLine, playerNum = self.getToken(currLine,currpos,Lines)
            treeNode.player = int(playerNum)
            currpos, currLine, infoset = self.getToken(currLine,currpos,Lines)
            treeNode.infoset = int(infoset)
            currpos, currLine, infosName = self.getStringLiteral(currLine,currpos,Lines)
            currpos, currLine, token = self.getToken(currLine,currpos,Lines) # '{'
            while(self.checkStringLiteralPresent(currLine,currpos,Lines)):
                currpos, currLine, strLit = self.getStringLiteral(currLine,currpos,Lines)
                treeNode.action.append(strLit)

            currpos, currLine, token = self.getToken(currLine,currpos,Lines) # '}'
            currpos, currLine, token = self.getToken(currLine,currpos,Lines) # outcomeVal
        else:
            currpos, currLine, nodeName = self.getStringLiteral(currLine,currpos,Lines)
            treeNode.nodeName = nodeName  
            currpos, currLine, outcomeVal = self.getToken(currLine,currpos,Lines)
            currpos, currLine, outcomeName = self.getStringLiteral(currLine,currpos,Lines)
            currpos, currLine, token = self.getToken(currLine,currpos,Lines) # '{'
            utilVals = ''
            currpos, currLine, token = self.getToken(currLine,currpos,Lines)
            while token!='}':
                utilVals = utilVals + token
                currpos, currLine, token = self.getToken(currLine,currpos,Lines)
            utilList = utilVals.split(",")
            for ut in utilList:
                ut = ut.strip()
                ut = float(ut)
                treeNode.utilV.append(ut)
                
        return currpos,currLine, treeNode                
            
        
    def checkStringLiteralPresent(self,currLine,currPos,Lines):
        line = Lines[currLine]
        lineSize = len(line)
        flag = True
        separators = [' ','\t','\r']
        while flag==True:
            while currPos<lineSize and line[currPos] in separators:
                currPos=currPos+1
            if currPos == lineSize:
                currPos = 0
                currLine=currLine+1
                if currLine==len(Lines):
                    flag=False
                    break
                line = Lines[currLine]
                lineSize = len(line)
            else:
                if(line[currPos]=='"'):
                    return True
                return False
        return False
    
    def getStringLiteral(self,currLine,currPos,Lines):
        strLit = ''
        line = Lines[currLine]
        lineSize = len(line)
        flag = True
        separators = [' ','\t','\r']
        while flag==True:
            while currPos<lineSize and line[currPos] in separators:
                currPos=currPos+1
            if currPos == lineSize:
                currPos = 0
                currLine=currLine+1
                if currLine==len(Lines):
                    flag=False
                    break
                line = Lines[currLine]
                lineSize = len(line)
            else:
                strLit+=line[currPos]
                currPos=currPos+1
                while currPos<lineSize and (line[currPos]!='"' or line[currPos-1]=='\\'):
                    strLit = strLit + line[currPos]
                    currPos = currPos+1
                strLit+=line[currPos]
                currPos = currPos + 1
                flag=False
                if currPos == lineSize:
                    currPos = 0
                    currLine=currLine+1
                    if currLine==len(Lines):
                        break
                    line = Lines[currLine]
                    lineSize = len(line)
        return currPos, currLine, strLit
                    
        
    def getToken(self,currLine,currPos,Lines):
        token = ''
        line = Lines[currLine]
        lineSize = len(line)
        flag = True
        separators = [' ','\t','\r']
        while flag==True:
            while currPos<lineSize and line[currPos] in separators:
                currPos=currPos+1
            if currPos == lineSize:
                currPos = 0
                currLine=currLine+1
                if currLine==len(Lines):
                    flag=False
                    break
                line = Lines[currLine]
                lineSize = len(line)
            else:
                while currPos< lineSize and line[currPos] not in separators:
                    token = token + line[currPos]
                    currPos = currPos+1
                flag=False
                if currPos == lineSize:
                    currPos = 0
                    currLine=currLine+1
                    if currLine==len(Lines):
                        break
                    line = Lines[currLine]
                    lineSize = len(line)
                    
        return currPos, currLine, token

class TreeNode:

    def __init__(self):
        self.par = None
        self.child = []
        self.action = []
        self.type=''
        self.player = 0
        self.infoset = 0
        self.nodeName=''
        self.utilV = []
        
class EFGCalc:
    
    def getStrategies(self,numpl, players, treeNode):
        infoSetVis = [[] for i in range(numpl+1)]
        strats = [[[]] for i in range(numpl+1)]
        stratsind = [[[]] for i in range(numpl+1)]
        
        strats,stratsind = self.recursStrat(strats,stratsind,infoSetVis,treeNode)
                        
        return stratsind, strats
    
    def recursStrat(self,strats,stratsind,infoSetVis,trNode):
        
        if trNode.type=='t':
            return strats,stratsind
        
        plnum = trNode.player
        infoSet = trNode.infoset
        acts = trNode.action
        child = trNode.child
        if infoSet not in infoSetVis[plnum]:
            stratpl = strats[plnum]
            stratsindpl = stratsind[plnum]
            newstratpl = []
            newstratindpl = []
            infoSetVis[plnum].append(infoSet)
            for j in range(len(stratpl)):
                currstrat = stratpl[j]
                currstratind = stratsindpl[j]
                for i in range(len(acts)):
                    newstrat = currstrat.copy()
                    newstratind = currstratind.copy()
                    act = acts[i]
                    act = act.strip("\"")
                    newstrat.append(act)
                    newstratpl.append(newstrat)
                    newstratind.append(i)
                    newstratindpl.append(newstratind)
                    
            strats[plnum].clear()
            strats[plnum] = newstratpl
            stratsind[plnum].clear()
            stratsind[plnum] = newstratindpl
                
        for ch in child:    
            strats,stratsind = self.recursStrat(strats,stratsind,infoSetVis,ch)
            
        return strats,stratsind
    
    def getActionsForInfoSet(self,numplayer,players,treeNode,infoSet):
        infMapping = [[[] for i in range(infoSet[j]+1)] for j in range(numplayer+1)]
        infMapping = self.recActionsInfMapping(numplayer,treeNode, infoSet,infMapping)
        return infMapping
    
    def recActionsInfMapping(self,numplayer,treeNode,infoSet,infMapping):
        if treeNode.type == 'p':
            pln = treeNode.player
            infs = treeNode.infoset
            if len(infMapping[pln][infs])==0:
                for i in treeNode.action:
                    infMapping[pln][infs].append(i)
            for ch in treeNode.child:
                infMapping = self.recActionsInfMapping(numplayer,ch,infoSet,infMapping)
        return infMapping
                    
    
    def getInfoSetMap(self, trNode, plnum):
        
        infoSetNum = [0 for i in range(plnum+1)]
        self.recInfoSet(trNode, infoSetNum, plnum)
        return infoSetNum
    
    def recInfoSet(self, trNode, infoSetNum, plnum):
        if trNode.type=='t':
            return infoSetNum
        
        pln = trNode.player
        infoSetNum[pln] = max(infoSetNum[pln],trNode.infoset)
        for ch in trNode.child:
            infoSetNum = self.recInfoSet(ch,infoSetNum,plnum)
        
        return infoSetNum
    
    def getUtilities(self,currstate,numplayer,treeNode):
        
        if treeNode.type=='t':
            return treeNode.utilV
        infs = treeNode.infoset
        pln = treeNode.player
        suggestAct = currstate[pln][infs]
        ch = treeNode.child[suggestAct-1]
        return self.getUtilities(currstate,numplayer,ch)
    
    def updateCurrState(self,currstate,numplayer,infoSet,infActionMapping):
        pl = 1
        flag = False
        while pl<=numplayer and flag==False:
            actionstate = currstate[pl]
            actionCh = 1
            for i in range(len(currstate[pl])-1,0,-1):
                if actionstate[i]!=len(infActionMapping[pl][i]):
                    flag = True
                    actionCh = i
                    break
            if flag==True:
                for j in range(pl):
                    for k in range(len(currstate[j])):
                        currstate[j][k] = 1
                currstate[pl][actionCh] = currstate[pl][actionCh] + 1
                for j in range(actionCh+1,len(currstate[pl])):
                    currstate[pl][j] = 1
            pl = pl+1
        return currstate
    
    def getSPNE(self,treeNode,numplayer):
        
        if treeNode.type=='t':
            spnes = [[[] for i in range(numplayer)]]
            utilities = [treeNode.utilV]
            return spnes, utilities

        pln = treeNode.player
        spnechs = []
        utilitchs = []
        act = treeNode.action
        numstr = [0 for i in range(len(act))]
        #print('UCHS', utilitchs)
        
        numiter=1
        for i in range(len(treeNode.child)):
            spn, uti = self.getSPNE(treeNode.child[i],numplayer)
            spnechs.append(spn)
            utilitchs.append(uti)
            numstr[i] = len(uti)
            numiter = numiter * numstr[i]
            
        currstate = [0 for i in range(len(numstr))]
        statelist = [[] for i in range(len(treeNode.child))]
        utilList = [[] for i in range(len(treeNode.child))]
        
        #print('start ', numiter, numstr)
        for i in range(numiter):
            #print('cs: ', currstate)
            currutillist = []

            #create list of children utilities for current state for pln player
            for j in range(len(utilitchs)):
                stratnum = currstate[j]
                currutil = utilitchs[j][stratnum][pln-1]
                currutillist.append(currutil)
            #print('CUL:', currutillist, pln)
            maxv = max(currutillist)
            
            #print('Curst', currstrat)
            
            favchild = []
            newstratlist = []
            for j in range(len(treeNode.child)):
                if currutillist[j]==maxv:
                    favchild.append(j)
            #print('Fchild: ', favchild, currstate)
                    
            for j in range(len(favchild)):
                x = favchild[j]
                csc = currstate.copy()
                jchildutillist = utilitchs[x][currstate[x]]
                jcu = jchildutillist.copy()
                utilList[x].append(jcu)
                statelist[x].append(csc)
                
            k=len(currstate) - 1
            while k>=0:
                if(currstate[k]!=(numstr[k]-1)):
                    currstate[k]=currstate[k]+1
                    for y in range(k+1,len(currstate)):
                        currstate[y]=0
                    break
                k = k-1
                
        #print('StateList', statelist)
        #print('UtilList', utilList)
        
        spnes = []
        utils = []
        
        for i in range(len(treeNode.child)):
            for j in range(len(statelist[i])):
                strat = [[] for pl in range(numplayer)]
                stateRec = statelist[i][j]
                for k in range(len(stateRec)):
                    statek = stateRec[k]
                    for p in range(numplayer):
                        actionsforstrat = spnechs[k][statek][p-1]
                        for acs in actionsforstrat:
                            acs = acs.strip('\"')
                            strat[p-1].append(acs)
                strat[pln-1].insert(0,treeNode.action[i].strip('\"'))
                spnes.append(strat)
                utils.append(utilList[i][j])
        #print(spnes)
                
        return spnes, utils
        
        


                 
        


