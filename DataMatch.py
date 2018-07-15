#coding=utf-8
#!/usr/bin/python

import random
import sys   
sys.setrecursionlimit(10000)

UPLIMIT = 257660.0  #257660.28
NUMBERS = 101

#发票金额基础数据
InvoiceData=[
64000.00,
2772.00,
9504.00,
7830.00,
50616.00,
2142.00,
13566.00,
38646.00,
4773.60,
4492.80,
4212.00,
578.00,
5236.00,
2500.00,
800.00,
7830.00,
2700.00,
3060.00,
1710.00,
1019.20,
544.00,
12996.00,
7125.00,
1578.00,
3822.00,
1368.00,
19278.00,
12994.80,
-623.3         
             ]
                          
def solve(numlist):
    if UPLIMIT >= 1000 and NUMBERS >= 100:
        numlist.sort()        
        print (numlist)
        (finalResults, unMatchedNums) = baseSolve(numlist, matchSumUnrec)
    else:
        numlist.sort()             
        print (numlist)
        (finalResults, unMatchedNums) = baseSolve(numlist, matchSum)
    improve(finalResults, unMatchedNums)
    return (finalResults, unMatchedNums)

def baseSolve(numlist, matchSum):    
    if not numlist or len(numlist) == 0:
       return ([],[]);
    finalResults = []
    unMatchNums = []
    while len(numlist) > 0: 
        num = numlist.pop()
        matched = []
        if matchSum(UPLIMIT-num, numlist, matched):
            removelist(numlist, matched)
            matched.append(num)        
            finalResults.append(matched)
        else:
            unMatchNums.append(num)
    return (finalResults, unMatchNums)       

def removelist(origin, toberemoved):
    for e in toberemoved:
        if e in origin:
           origin.remove(e)

def copylist(numlist):
    return [num for num in numlist]

def matchSum(rest, restlist, prematched):
        
    if rest > 0 and len(restlist) == 0:
        return False

    if rest > 0 and len(restlist) == 1 and restlist[0] != rest:
        return False

    if rest > 0 and len(restlist) == 1 and restlist[0] == rest:
        prematched.append(restlist[0])
        return True

    getone = restlist[0]
    if rest > getone:
        prematched.append(getone)
        if matchSum(rest-getone, restlist[1:], prematched):
            return True
        else:
            prematched.remove(getone)
            return matchSum(rest, restlist[1:], prematched)
    elif rest == getone:
        prematched.append(getone)
        return True;
    else:
        return matchSum(rest, restlist[1:], prematched)


def matchSumUnrec(asum, sortedlist, matched):
    
    if asum > 0 and len(sortedlist) == 0:
        return False

    if asum > 0 and len(sortedlist) == 1 and sortedlist[0] != asum:
        return False

    if asum > 0 and len(sortedlist) == 1 and sortedlist[0] == asum:
        matched.append(sortedlist[0])
        return True

    tmpsum = 0
    ind = 0
    size = len(sortedlist)
    while ind < size:
        num = sortedlist[ind]
        tmpsum += num
        if tmpsum < asum:
            matched.append(num)
            ind += 1
            continue
        elif tmpsum == asum:
            matched.append(num)
            return True
        else:
            tmpsum -= num
            break
   
    need = asum - tmpsum
    tosearch = map(lambda x:x+need, matched)
    restlist = sortedlist[ind:]
    
    for e in tosearch:
        if e in restlist:
            matched.append(e)
            matched.remove(e-need)
            return True

    return False
    

def improve(finalResults, unMatchedNums):
    for comb in finalResults:
        for num in comb:
            matched = []
            if matchSum(num, unMatchedNums, matched) and len(matched) > 1:
                print ('Improved: ' , num, ' ', matched)
                comb.remove(num)
                comb.extend(matched)
                unMatchedNums.append(num)
                for e in matched:
                    unMatchedNums.remove(e)
                if len(unMatchedNums) == 0:
                    return

def printResult(finalResults, unMatchedNums, numlist):
    
    f_res = open('res.txt', 'w')
    f_res.write('origin: ' + str(numlist) + '\n')
    f_res.write('averag: ' + str((float(sum(numlist))/len(numlist))) + '\n')
    f_res.write('solution: ')
    
    usedNums = 0
    finalNumList = []
    for comb in finalResults:
        f_res.write(str(comb) + ' ')
        assert sum(comb) == UPLIMIT
        usedNums += len(comb)
        finalNumList.extend(comb)
    finalNumList.extend(unMatchedNums)
    f_res.write('\nUnMatched Numbers: ' + str(unMatchedNums) + '\n')
    f_res.write('Used numbers: %s, UnMatched numbers: %d.\n' % (usedNums, len(unMatchedNums)))

    f_res.write('origin: %d , final: %d\n' % (len(numlist), len(finalNumList)))
    for e in finalNumList:
        numlist.remove(e)
    if len(numlist) > 0:
        f_res.write('Not Occurred numbers: ' + str(numlist))
    
    f_res.close() 


def ToMatch(numlist):
    MatchList1 =[]
     
    for e in numlist:
        if e <=UPLIMIT:
           MatchList1.append(e)

    newnumlist = copylist(MatchList1)
    #newnumlist = copylist(numlist)
    (finalResults, unMatchedNums) = solve(newnumlist)

    newnumlist = copylist(numlist)
    printResult(finalResults, unMatchedNums, newnumlist)

if __name__ == '__main__':    
    ToMatch(InvoiceData)
    
    
