
def getSetID(d,pt):
	if pt in d.keys():
		return d[pt]
	else:
		return None

def checkCycle(d,pt1,pt2):
	if d[pt1]==d[pt2]:
		return True
	else:
		return False

def checkExistingGrid(d,setID,n):
	#print "checking existing grid in set"
	#print setID
	for key,value in d.iteritems():
		#print value
		if value==setID:
			if key>n:
				return True
	return False
	

def addtoSet(d,setID,pt2):
	#print "add to set"
	d[pt2]=setID
		

# def main():
# 	d={}
# 	existingList=[None]*10
# 	addtoSet(d,0,10,9,existingList)
# 	addtoSet(d,0,1,9,existingList)
# 	print checkIfFirstExistingGrid(d,0,existingList)
# 	print getSetID(d,0)
# 	print checkCycle(d,1,10)

if __name__=='__main__':
	main()