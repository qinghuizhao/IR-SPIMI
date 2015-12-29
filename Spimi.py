import re
import sys
import pickle
import string
import math
import gamma
#import Tokenizer as tk
"""
IdToToken (token,docid)


about regular expression

# input: "A first-class ticket to the U.S.A. isn't expensive?"
# output: ['A', 'first-class', 'ticket', 'to', 'the', 'U.S.A.', "isn't", 'expensive', '?']
# return re.findall("(?:[A-Z]\.)+|\w+(?:[-']\w+)*|[-.(]+|\S\w*", text)



"""

TokenToidDict = {}
LocalTokenDict = {}
DocIdToDocName = {}
Count = 1
Id_DOCNO_Title = {}


Total_Terms = 0
Total_Tokens = 0
Total_docToken = []


remap = {ord('\t') : ' ' , ord('\n') : ' ' , ord('\r') : None}

def tokenize(text):
	return re.findall("[A-Z|a-z]+[0-9]*",text)

def parse(filepath):
	f = open(filepath,'r')
	regTEXT   = re.compile(r'(?<=<DOC>).*?(?=</DOC>)',flags=re.DOTALL)
	regNO = re.compile(r'(?<=<DOCNO>).*?(?=</DOCNO>)', flags=re.DOTALL)
	regTitle = re.compile(r'(?<=<title>).*?(?=</title>)', flags=re.DOTALL)
	#Total_Tokens += len(regTEXT) + len(regNO) + len(regTitle)

	token_stream = []
	text = f.read()

	global Count, Total_Tokens, Total_Terms
	#global remap
	for body in regTEXT.findall(text):
		StringNo = regNO.findall(body)
		tmpstr = tokenize(body.lower())

		for tkn in tmpstr:
			
			if tkn not in TokenToidDict:
				TokenToidDict[tkn] = [Count]
			else:
				if Count not in TokenToidDict[tkn]:
					TokenToidDict[tkn].append(Count)
		newtile = regTitle.findall(body)

		total_each_doc_token = len(StringNo) + len(tmpstr) + len(newtile)

		Total_docToken.append(total_each_doc_token)

		Total_Tokens += total_each_doc_token

		newtile2 = []
		for char in newtile:
			newchar = char.replace('\t', ' ')
			newchar1 = newchar.replace('\n', ' ')
			newtile2.append(newchar1)
		#newtile2.append('$')

		newtile2 = str(newtile2)
		if newtile2:
			#newtile += '$'
			#p=re.compile('\s+') 
			#newtile = newtile.translate(remap) 
			newtitle2 = newtile2.replace('\t',' ')
			
			
		DocIdToDocName[Count] = [StringNo,newtile2]
		Count += 1
		#print "Count:%d" % Count


	for k,v in DocIdToDocName.iteritems():
		print "%d : %s %s" % (k,v[0],v[1])

	#	print "%d : %s" % (k,v[1])




def mergeIndex(fullindex,littleindex):
	for key in littleindex:
		if key in fullindex:
			for idx in littleindex[key]:
				if idx not in fullindex[key]:
					fullindex[key].append(idx)
		else:
			fullindex[key] = littleindex[key]
	return fullindex

#A = {'kui' : [1,2,3,4,5],'Whaha' : [1,2,3]}

def loadtodict(filepath):
	f = open(filepath,'rb')
	dict = pickle.load(f)
	#print(dict)
	f.close()
	return dict

def writetofile(dict,filepath):
	f = open(filepath,'wb')
	pickle.dump(dict,f)
	f.close()

#writetofile(A,"H:/fullindex.txt")
#loadtodict(TokenToidDict,"H:/fullindex.txt")


def SPIMI():
	finalpath = "./finalresult.txt"
	finalpickle = './finalpickle.pic'
	dictpath = "./dict.txt"
	f = open(finalpath,'wb')
	global LocalTokenDict
	global TokenToidDict, Total_Terms, Total_Tokens
	for i in range(1,5):
		#print("Haha {}".format(i))
		filepath = "./shakespeare/trec."+str(i)
		outputfilepath = "./dictmidfile.txt"
		DocIdToDocName.clear()
		TokenToidDict.clear()
		LocalTokenDict.clear()
		parse(filepath)
		if i != 1:
			LocalTokenDict = loadtodict(outputfilepath)
		LocalTokenDict = mergeIndex(LocalTokenDict,TokenToidDict)
		writetofile(LocalTokenDict,outputfilepath)
	
	keys = sorted(LocalTokenDict.keys())

	dictw = open(dictpath,"wb")
	#worderdict = sorted(LocalTokenDict, key = lambda x : x.key)
	for k in keys:
		dictw.write(k)
		#dictw.write("\t")
	dictw.write("\n")
	st = 0
	for k in keys:
		dictw.write(str(st))
		dictw.write("\t")
		dictw.write(str(len(k)+st))
		st = st + len(k)
		dictw.write("\n")
	dictw.close()

	Total_Terms = len(keys)


	keys = sorted(keys)
	fpickle = open(finalpickle,'wb')

	pickle.dump(LocalTokenDict,fpickle)




	for value in keys:
		f.write(value)
		f.write("\t")
		f.write(str(LocalTokenDict[value]))
		f.write("\n")
	f.close()

	print "Tokens:%d" % Total_Tokens
	print "Gamma code of Terms is : %s" % (gamma.Gamma_encode(Total_Tokens))
	print "Terms:%d" % Total_Terms
	print "Gamma code of Terms is : %s" % (gamma.Gamma_encode(Total_Terms))
	print Total_docToken
	print "Average tokens of Doc:%d " % (Total_Tokens/22)


if __name__ == '__main__':
	SPIMI()

