import math
import random
import csv

def main():
    trainFile = open('train.csv')
    testFile=open('test.csv')
    trainAttribute = "Cover_Type"
    trainData = []
    testData=[]
    recursion=0
    fd=[]
    for tF in trainFile:
        tF = tF.strip("\r\n")
        tF = tF.split(',')
        del tF[0]
        trainData.append(tF)
    
    attributesAll=trainData[0] 
    trainData.remove(attributesAll)
    tree=createTree(recursion,trainAttribute,attributesAll,trainData)    
    for f in testFile:
        f=f.strip('\r\n')
        f=f.split(',')
        fd.append(f[0])
        del f[0]
        testData.append(f)
    testData.remove(testData[0])
    re=predict(attributesAll,tree,testData) 
    writer=csv.writer(open('result.csv','w',newline=''))    
    for j in range(len(re)):
        writer.writerow([fd[j],re[j]])
        
        
def createTree(rec,trainAttribute,attributesAll,trainData):
    rec += 1
    trainData = trainData[:] 
    sets = [tD[attributesAll.index(trainAttribute)] for tD in trainData]
        
    default = mostCommonAttriVal(trainAttribute,attributesAll,trainData)
    if not trainData or (len(attributesAll) - 1) <= 0:
        return default
    elif sets.count(sets[0]) == len(sets):
        return sets[0]
    else:
        bestAttribute = chooseBestAttri(trainAttribute, attributesAll,trainData)
        tree = {bestAttribute:{}}
        for colValue in getColVal(bestAttribute,attributesAll,trainData):
            currSet = getCurrentVal(bestAttribute,colValue,attributesAll,trainData)
            nextAtr = attributesAll[:]
            nextAtr.remove(bestAttribute)
            smalltree = createTree(rec,trainAttribute,nextAtr,currSet)
            tree[bestAttribute][colValue] = smalltree
    return tree
    
def mostCommonAttriVal(trainAttribute,attributesAll,trainData):
    dictQ = {}
    index = attributesAll.index(trainAttribute)
    for t in trainData:
        if t[index] in dictQ:   
            dictQ[t[index]] += 1 
        else:
            dictQ[t[index]] = 1
    counter = 0
    mostCommomAttributeValue = ""
    for k in dictQ.keys():
        if dictQ[k]>counter:
            counter = dictQ[k]
            mostCommomAttributeValue = k
    return mostCommomAttributeValue
    
def chooseBestAttri(trainAttribute,attributesAll,trainData):
    bestAttribute = attributesAll[0]
    initGain = 0;
    for attri in attributesAll:
        postGain = infoGain(attri, trainAttribute,attributesAll, trainData) 
        
        if postGain>initGain:
            initGain = postGain
            bestAttribute = attri
    return bestAttribute    
    
def getColVal(bestAttribute,attributesAll,trainData):
    pointer = attributesAll.index(bestAttribute)
    datas = []
    for entry in trainData:
        if entry[pointer] not in datas:
            datas.append(entry[pointer])
    return datas
    
def getCurrentVal( bestAtrribute, colValue,attributesAll,trainData):
    currSet = [[]]
    numb = attributesAll.index(bestAtrribute)
    for tD in trainData:
        if (tD[numb] == colValue):
            sets = []
            for r in range(0,len(tD)):
                if(r != numb):
                    sets.append(tD[r])
            currSet.append(sets)
    currSet.remove([])
    return currSet
    
def infoGain(attri, trainAttribute,attributesAll, trainData):
    dictQuant = {}
    smallEntropy = 0.0
    i = attributesAll.index(attri) 
    for train in trainData:
        if train[i] in dictQuant:
            dictQuant[train[i]] += 1.0
        else:
            dictQuant[train[i]]  = 1.0
            
    for dq in dictQuant.keys():
        freq = dictQuant[dq] / sum(dictQuant.values())
        dataSet     = [da for da in trainData if da[i]==dq]
        smallEntropy += freq * calculateEntropy(trainAttribute,attributesAll, dataSet)
    compEntropy=calculateEntropy(trainAttribute,attributesAll, trainData) 
    return (compEntropy - smallEntropy)
    
def calculateEntropy(trainAttribute,attributesAll, trainData):

    dataQuant = {}
    ent = 0.0
    i = 0
    for atall in attributesAll:
        if (trainAttribute == atall):
            break
        ++i
    for tD in trainData:
        if tD[i] in dataQuant:
            dataQuant[tD[i]] += 1.0
        else:
            dataQuant[tD[i]]  = 1.0
        
    for q in dataQuant.values():
        ent += (-q/len(trainData)) * math.log(q/len(trainData), 2) 
        
    return ent    

def predict(attributesAll,tree,testData):
    count=0
    r=['Cover_Type']
    for e in testData:
        count+=1
        tempD=tree.copy() 
        result=""
        while (isinstance(tempD,dict)):
            val=list(tempD.keys())[0]
            tempD=list(tempD.values())[0]
            index=attributesAll.index(val)
            value=e[index]
            if(value in tempD.keys()):
                result=tempD[value]
                tempD=tempD[value]
            elif (((int(value)-1) in tempD.keys()) or ((int(value)-2) in tempD.keys()) or ((int(value)-3) in tempD.keys()) or ((int(value)-4) in tempD.keys()) or ((int(value)-5) in tempD.keys()) or ((int(value)+1) in tempD.keys()) or ((int(value)+2) in tempD.keys()) or ((int(value)+3) in tempD.keys()) or ((int(value)+4) in tempD.keys()) or ((int(value)+5) in tempD.keys()) or ((int(value)+6) in tempD.keys()) or ((int(value)-7) in tempD.keys()) or ((int(value)-8) in tempD.keys()) or ((int(value)-9) in tempD.keys()) or ((int(value)-10) in tempD.keys()) or ((int(value)+6) in tempD.keys()) or ((int(value)+7) in tempD.keys()) or ((int(value)+8) in tempD.keys()) or ((int(value)+9) in tempD.keys()) or ((int(value)+10) in tempD.keys())):
                        result=tempD[value]
                        tempD=tempD[value]
            else:
                result=random.randint(1,7)
                break
        r.append(result)
    return(r)

if __name__ == '__main__':
    main()