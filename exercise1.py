#Anastasios Tzinieris
#2554
import csv
import sys


max=[]
Wk={}
playersLb={}
playersUb={}
playerExist={}
playerMissing={}


def access(statFile):
    lines=[]
    for i in range(len(statFile)):
        line=list(map(int, statFile[i].readline().strip('[]').split(',')))
        lines.append(line)
    return lines


def statScore(stat,max):
    score=float(stat/max)
    return score


def findMax(statLine):
    max=[]
    for i in range(len(statLine)):
        max.append(statLine[i][1])
    return max


def updateLb(statLine,score):
    global playersLb
    if(statLine in playersLb):
        playersLb[int(statLine)]=playersLb.get(statLine,"none") + score
    else:
        playersLb[int(statLine)]=score


def updateUb(line):
    global playerMissing
    global playerExist
    global playersLb
    global playersUb
    global max

    km=0
    for i in playersUb:
        if(i not in Wk):
            for j in range(len(playerMissing[int(i)])):
                k=playerMissing[int(i)]
                km=km+statScore(line[k[j]-1][1],max[k[j]-1])
            playersUb[i]=playersLb[i]+km


def playerInFileExists(player,iterator):
    global playerExist
    global playerMissing
    if(player in playerExist):
        playerExist[int(player)].append(iterator+1)
        playerMissing[int(player)].remove(iterator+1)
    else:
        inFile=[]
        inFile.append(iterator+1)
        playerExist[int(player)]=inFile


def playerInFileMissing(player,len):
    global playerMissing
    global playerExist
    nonFound=[]
    k=0
    for i in range(len):
        if ((i+1) in playerExist[int(player)]):
            k=1
        else:
            nonFound.append(i+1)
            playerMissing[int(player)]=nonFound


def updateWk(k):
    global playersLb
    global Wk
    j=0
    Wk={}
    for i in sorted(playersLb.items(), key = lambda kv:(kv[1], kv[0]),reverse=True):
        if(j<k):
            Wk[i[0]]=i[1]
            j+=1


def nra():
    global Wk
    check=1
    minLb=sorted(Wk.items(), key = lambda kv:(kv[1], kv[0]),reverse=False)[0][1]
    for i in playersUb:
        if(minLb<playersUb[i] and i not in Wk):
            check=0
            return check
    return check


def lara(files,k):
    global Wk
    global playersUb
    global playersLb
    global playerExist
    global playerMissing
    global max

    k=int(k)
    statFile=[]
    for i in range(len(files)):
        if(files[i]==1):
            trb=open("2017_TRB.csv",'r')
            statFile.append(trb)
        elif(files[i]==2):
            ast=open("2017_AST.csv",'r')
            statFile.append(ast)
        elif(files[i]==3):
            stl=open("2017_STL.csv",'r')
            statFile.append(stl)
        elif(files[i]==4):
            blk=open("2017_BLK.csv",'r')
            statFile.append(blk)
        elif(files[i]==5):
            pts=open("2017_PTS.csv",'r')
            statFile.append(pts)
        else:
            print("error")

    statLine=access(statFile)
    numberOfAccesses=1
    max=findMax(statLine)

    T=0
    for i in range(len(statLine)):
        score=statScore(statLine[i][1],max[i])
        T=T+score
        updateLb(statLine[i][0],score)
        playerInFileExists(statLine[i][0],i)
        playerInFileMissing(statLine[i][0],len(statLine))
        if(statLine[i][0] not in playersUb):
            playersUb[int(statLine[i][0])]=playersLb[int(statLine[i][0])]
    t=0
    updateWk(k)
    while(statLine!=''):
        statLine=access(statFile)
        numberOfAccesses+=1
        if(t<T or len(Wk)!=k):
            T=0
            for i in range(len(statLine)):
                score=statScore(statLine[i][1],max[i])
                T=T+score
                updateLb(statLine[i][0],score)
                playerInFileExists(statLine[i][0],i)
                playerInFileMissing(statLine[i][0],len(statLine))
            updateWk(k)
        else:
            #print(t)
            for i in range(len(statLine)):
                if(statLine[i][0] in playersLb):
                    score=statScore(statLine[i][1],max[i])
                    updateLb(statLine[i][0],score)
                    playerInFileExists(statLine[i][0],i)
                    playerInFileMissing(statLine[i][0],len(statLine))
                    if(statLine[i][0] not in playersUb):
                        playersUb[int(statLine[i][0])]=playersLb[int(statLine[i][0])]
            updateUb(statLine)
            updateWk(k)
            check=nra()
            if(check==1):
                break
        t=sorted(Wk.items(), key = lambda kv:(kv[1], kv[0]),reverse=False)[0][1]
    print(numberOfAccesses)
    print(Wk)


def main():
    fileList = list(map(int, sys.argv[1].strip('[]').split(',')))
    lara(fileList,sys.argv[2])


if __name__ == "__main__":
    main()
