import os, sys, re, csv

def readTable(tablePath):
        with open(tablePath,"r") as f:
                rd=csv.reader(f, delimiter='\t')
                out = [[j for j in i if len(j) > 0] for i in rd]
        if not len(out) > 0:
                raise Exception("No rows in the translation table. stop.")
        if not len(out[0])%2 == 0:
                raise Exception("Odd number of columns in translation table. stop")
        return out
                
def convert(filePath,trans):
        replace = []
        path,name = os.path.split(filePath)
        for i in trans:
                match = [re.search(v,name) for j,v in enumerate(i) if j%2==0]#look for translation table matches in even numbered columns
                #print match
                if not None in match:
                    replace.append(i)
        if len(replace) > 1:
                raise IOError("Replacement not unique, found the following matching rows: {0}".format("\n".join([i.__str__() for i in replace])))
        if len(replace) == 0:
                raise IOError("No replacements found for this file. stop.")
        for i,v in enumerate(replace[0]):
                if i % 2 == 0: #we're in a match column
                        print "Found a replacement row: {0}".format( replace[0] )
                        name = re.sub(v,replace[0][i+1],name)
        os.rename(filePath,os.path.join(path,name))

def fixNames(dirName,trans):#rename the files coming out of imagemagick
        files=os.listdir(dirName)
        for i in files:
                mtch = re.search("_bx(\d+).tif$",i)
                if mtch:
                        num = int(mtch.groups()[0])
                        if num>2: #3 through 5:
                                num -=2
                                color = "GRN"
                        elif num <=2: #0 through 2:
                                num +=1
                                color = "RED"
                        newName = re.sub("_bx\d+.tif$"," {0} _b{1}.tif".format(color,num),i)
                        newName = os.path.join(dirName,newName)
                        oldName = os.path.join(dirName,i)
                        print "Changing names: {0} to {1}".format(oldName,newName)
                        os.rename(oldName,newName)
                        try:
                                convert(newName,trans)
                        except IOError as e:
                                print "found bx match but skipped converting {0}".format(newName)
                                print e
                else:
                        print "did not find bx match so skipped converting {0}".format(i)

if __name__ == "__main__":
	dirToEdit="".join(sys.argv[1].split('"'))
	translation=sys.argv[2]
	fixNames(dirToEdit, readTable(translation))
