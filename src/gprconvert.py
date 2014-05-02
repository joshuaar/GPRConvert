#!/usr/bin/env python
import argparse
import os
import re
import sys
import numpy as np
import Data
def getFileList(path, r=False): # get list of GPR files in a path
    out = filter(lambda x: x.endswith("gpr"),os.listdir(path))
    paths = [os.path.abspath(os.path.join(path,i))for i in out] # return the abspaths
    if not r:
        return paths
    return paths + [j for i in getDirList(path) for j in getFileList(i)]

def getDirList(path):
    return [os.path.join(path,i) for i in os.listdir(path) if os.path.isdir(os.path.join(path,i))]

def getColNames(filePath):
    rowNum = detectDataStart(filePath)
    with open(filePath,mode="r") as f:
        for i in range(rowNum):
            f.readline()
        out = f.readline()
    return out.replace('"','').rstrip().split("\t")

def detectDataStart(filePath,nRowsToSearch=100):
    lines = []
    with open(filePath,mode="r") as f:
        for i in range(nRowsToSearch):
            row = f.readline()
            lines.append(len(row))
    return lines.index(max(lines))

def findCorrectCols(filePath,idPattern,dataPattern):
    colNames = getColNames(filePath)
    idCols = [i for i in colNames if not re.search(idPattern,i)==None]
    dataCols = [i for i in colNames if not re.search(dataPattern,i)==None]
    if len(idCols) > 1:
        print "More than one possible ID column: {0}\n, taking leftmost by default".format(", ".join(idCols))
    if len(dataCols) > 1:
        print "More than one possible Data column: {0}\n, taking leftmost by default".format(". ".join(dataCols))
    id,dat = (idCols[0],dataCols[0])
    idCol = colNames.index(id)
    dataCol = colNames.index(dat)
    return idCol,dataCol

def readGPR(filePath,idCol,dataCol):
    skip = detectDataStart(filePath)+1
    with open(filePath,mode="r") as f:
        raw = [i.replace('"','').rstrip().split("\t") for i in f]
    raw = raw[skip:]
    id = [i[idCol] if len(i)>idCol else "" for i in raw]
    data = [i[dataCol] if len(i) > dataCol else "0" for i in raw]
    return id,data

def extractCols(path,idPattern,dataPattern):
    '''Converts one GPR indicated by path into 2 columns, one for data, one for peptide ids'''
    idCol,dataCol = findCorrectCols(path,idPattern,dataPattern)
    return readGPR(path,idCol,dataCol)

def extractDir(files,idPattern="Name",dataPattern="F.*Median$"):
    out = [extractCols(i,idPattern,dataPattern) for i in files]
    firstLastIDs = [(i[0][0],len(i[0]),i[0][-1]) for i in out]
    _reduceFun = lambda x,y: x==y and x or None # if x == y return x, else return None	
	start = firstLastIDs[0]
	idsAreEqual = True
	for i,v in enumerate(firstLastIDs):
		res = _reduceFun(start,v)
		if res:
			start = res
		else:
			print "Mismatched IDs on {0} with value {1}".format(files[i],v)
			idsAreEqual = False
    if not idsAreEqual:
        raise Exception("Peptide IDs don't match across files. Were these run on the same arrays?")
    peps = out[0][0]
    vals = [[float(j) for j in i[1]] for i in out] # convert values to integers
    vals = np.array(zip(*vals))
    samples = files
    return peps,vals,samples

def writeExtracted(destination,extracted):
    peps,vals,samples=extracted
    with open(destination,mode="w") as f:
        f.write("\t".join(["ID"]+[os.path.basename(i) for i in samples])+"\n")
        for i in range(vals.shape[0]):
            pep = peps[i]
            val = vals[i,:]
            f.write(pep+"\t")
            f.write("\t".join([str(i) for i in val])+"\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert gpr files to csv")
    parser.add_argument("convert", nargs="+", help="Directories to convert")
    parser.add_argument('-r',help="Recursive conversion", action="store_true")
    parser.add_argument('-d',help="Destination", nargs=1)
    parser.add_argument('-w',help="Wavelength",nargs=1)
    args = parser.parse_args()
    source = args.convert[0]
    destination = "parsed.csv"
    print source
    if args.d:
        destination = args.d[0] 
    files = getFileList(source,args.r)
    if len(files) == 0:
        raise Exception("No GPRs to convert")
    for i in files:
        print i
    if not args.w:
        x=extractDir(files)
    else:
        x=extractDir(files,dataPattern="F{0} Median$".format(args.w[0]))
    if destination:
        writeExtracted(destination,x)
    
    
