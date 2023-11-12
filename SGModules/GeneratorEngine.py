import random

siz = 9
#size of subcell row, column
srow = 3
scol = 3
div = [3,3]
posnum = set()
sudoku = list()
slvdsudoku = list()
ccn = 0
gl = []
indeadend = 0


class SavedStatus():
	def __init__(self, sdk, row, col, vn):
		self.sdk = sdk
		self.row = row
		self.col = col
		self.vn = vn


#Inherited (with small changes) from solver
def coherencychecker(sdk):
	global div
	global siz
	
	#Check columns
	for cntr in range(siz):
		#initialise list of elements to be checked
		vl = set()
		for cntc in range(siz):
			#Check only nonblanks
			if sdk[cntr][cntc] != 0:
				if sdk[cntr][cntc] in vl:
					return False
				else:
					vl.add(sdk[cntr][cntc])
	#Check rows
	for cntc in range(siz):
		#initialise list of elements to be checked
		vl = set()
		for cntr in range(siz):
			#Check only nonblanks
			if sdk[cntr][cntc] != 0:
				if sdk[cntr][cntc] in vl:
					return False
				else:
					vl.add(sdk[cntr][cntc])
	#Check for cell groups
	for cnt in range(div[0]*div[1]):
		vl = set()
		ro, co = int((cnt - cnt % div[1]) / div[1]) , cnt % div[1]
		#print("new")
		for cntr in range(div[1]*ro, div[1]*(ro + 1)):
			for cntc in range(div[0]*co, div[0]*(co + 1)):
				#Check only nonblanks
				#print(cntr,cntc)
				if sdk[cntr][cntc] != 0:
					if sdk[cntr][cntc] in vl:
						return False
					else:
						vl.add(sdk[cntr][cntc])
	return True

def blankcntr(sdk):
	blanks = 0
	for cntc in range(len(sdk)):
		blanks += sdk[cntc].count(0)
	return blanks

def CheckRow(row):
	global sudoku
	global siz
	rv = set()
	for cntc in range(siz):
		rv.add(sudoku[row][cntc])
	return rv


def CheckColumn(col):
	global sudoku
	global siz
	cv = set()
	for cntr in range(siz):
		cv.add(sudoku[cntr][col])
	return cv


def CheckCellGroup(row,col):
	#print("new")
	global sudoku
	global div
	sr, sc =  row - row % div[1], col - col % div[0]
	gv = set()
	for cntr in range(sr,sr+div[1]):
		for cntc in range(sc,sc + div[0]):
			#print(cntr,cntc)
			gv.add(sudoku[cntr][cntc])
	return gv


#This returns the values that could be possibly written into all cells
def CheckSolutions():
	global sudoku
	global siz
	global div
	global posnum
	ev = [[posnum.copy() for _ in range(siz)] for _ in range(siz)]
	#Check all cells
	for cntr in range(siz):
		for cntc in range(siz):
			if sudoku[cntr][cntc] == 0:
				#In blank cels, check possible solutions
				fc = CheckRow(cntr).union(CheckColumn(cntc).union(CheckCellGroup(cntr,cntc)))
				ev[cntr][cntc] = posnum.difference(fc)
			else:
				ev[cntr][cntc] = set()
	return ev


#In case there are cells where only one value can be written, this fills those cells with that value
def SimpleSolution(fv):
	global sudoku
	global siz
	global div
	global posnum
	#fv = CheckSolutions()
	rv = 0
	#Check all cells
	for cntr in range(siz):
		for cntc in range(siz):
			#This means that only one number would fit the given cell
			if len(fv[cntr][cntc]) == 1:
					#Insert to the given cell of the sudoku the only possible number not in the given row, column and subcellgroup, and return ready flag
					sudoku[cntr][cntc] = min(fv[cntr][cntc])
					rv = 1
	return rv


#Looks for cells with the only possible occurence of a value in the given row, column or subrectangle
def IntermediateSolution(fv):
	global sudoku
	global siz
	global div
	global posnum
	#fv = CheckSolutions()
	rv = 0
	for cntr in range(siz):
		for cntc in range(siz):
			if sudoku[cntr][cntc] == 0:
				#In every nonblank cell
				rl = set()
				cl = set()
				sl = set()
				#Get values from every other cell in the culomn
				for cntrr in range(siz):
					if cntrr != cntr:
						rl = rl.union(fv[cntrr][cntc])
				#Get values from every other cell in the row
				for cntcc in range(siz):
					if cntcc != cntc:
						cl = cl.union(fv[cntr][cntcc])
				#get values from every other cell in the subrectangle
				sr, sc =  cntr - cntr % div[1], cntc - cntc % div[0]
				for cntrr in range(sr, sr + div[1]):
					for cntcc in range(sc,sc + div[0]):
						if not (cntrr == cntr and cntcc == cntc):
							sl = sl.union(fv[cntrr][cntcc])
				#Check for all values occurrence
				for cnt in fv[cntr][cntc]:
					if cnt not in rl or cnt not in cl or cnt not in sl:
						#Case the given cell is the only place the current cnt value fits
						sudoku[cntr][cntc] = cnt
						rv = 1
						break
	return rv

def EliminateSolutions(fv):
	global siz
	global div
	global posnum
	#print(fv)
	doing = 1
	while doing == 1:
		doing = 0
		for cntg in range(div[0]*div[1]):
			ro, co = int((cntg - cntg % div[1]) / div[1]) , cntg % div[1]
			#Check for all possible values
			for cnt in posnum:
				rs = []
				cs = []
				#Check columnwise
				for cntr in range(div[1]*ro, div[1]*(ro + 1)):
					tv = 0
					for cntc in range(div[0]*co, div[0]*(co + 1)):
						if cnt in fv[cntr][cntc]:
							tv += 1
					rs.append(tv)
				#Check rowwise
				for cntc in range(div[0]*co, div[0]*(co + 1)):
					tv = 0
					for cntr in range(div[1]*ro, div[1]*(ro + 1)):
						if cnt in fv[cntr][cntc]:
							tv += 1
					cs.append(tv)
				#Eliminate rowwise
				#This means that value cnt can be found only in one row of the subcell
				if rs.count(0) == len(rs) - 1:
					for cntcc in range(siz):
						#This means outside the subcell
						if cntcc < div[0]*co or cntcc >= div[0]*(co + 1):
							if cnt in fv[div[1]*ro + rs.index(max(rs))][cntcc]:
								#If present, eliminate possible solution from all cells in the culomn that are not in the subrectangle
								fv[div[1]*ro + rs.index(max(rs))][cntcc] = fv[div[1]*ro + rs.index(max(rs))][cntcc].difference({cnt})
								doing = 1
				#Eliminate columnwise
				#This means that value cnt can be found only in one column of the subcell
				if cs.count(0) == len(cs) - 1:
					for cntrr in range(siz):
						#This means outside the subcell
						if cntrr < div[1]*ro or cntrr >= div[1]*(ro + 1):
							if cnt in fv[cntrr][div[0]*co + cs.index(max(cs))]:
								#If present, eliminate possible solution from all cells in the row that are not in the subrectangle
								fv[cntrr][div[0]*co + cs.index(max(cs))] = fv[cntrr][div[0]*co + cs.index(max(cs))].difference({cnt})
								doing = 1
	return fv

def HardSolution(fv):
	ev = EliminateSolutions(fv)
	t = SimpleSolution(ev)
	if t == 0:
		t = IntermediateSolution(ev)
	return t

#Number of possible solutions in each cell
def GetPosSol(fv):
	global siz
	global div
	global sudoku
	
	#Very high value means there is already a value in the given cell
	sols = [[10000000 for _ in range(siz)] for _ in range(siz)]
	for cntr in range(siz):
		for cntc in range(siz):
			#At least one solution can be fit in the given cell
			if len(fv[cntr][cntc]) != 0:
				sols[cntr][cntc] = len(fv[cntr][cntc])
			#No solutions can be fit into an empty cell
			elif sudoku[cntr][cntc] == 0:
				sols[cntr][cntc] = -1
	return sols

def GuessManager(sv):
	global sudoku
	global siz
	global gl
	global indeadend
	
	indeadend = 0
	
	ps = GetPosSol(sv)
	mv = min(min(ps[cnt]) for cnt in range(siz))
	cntr, cntc = 0,0
	#create shallow copy of sudoku
	lc = [[sudoku[cntr][cntc] for cntc in range(siz)] for cntr in range(siz)]
	
	#Case there is a cell with multiple solution where a choice has to be made, pick the smallest value
	if mv >= 2 and mv < 999999 and coherencychecker(sudoku):
		for cntr in range(siz):
			for cntc in range(siz):
				if ps[cntr][cntc] == mv:
					tl = list(sv[cntr][cntc])
					tl.sort()
					gl.append(SavedStatus(lc,cntr,cntc,0))
					sudoku[cntr][cntc] = tl[0]
					return 1
	
	#Case algorithm got stuck, needs to go back.
	if mv == -1 or mv > 999999 or coherencychecker(sudoku) != True:
		while True:
			if len(gl) > 0:
				lst = gl.pop()
				sudoku = lst.sdk
				fv = CheckSolutions()
				sv = EliminateSolutions(fv)
				rw = lst.row
				cl = lst.col
				if lst.vn <= len(sv[rw][cl]) - 2:
					#If there are still numbers to be tried in that position, do it (go to next smallest possible number not tried yet). Otherwise, do nothing(go one further step back in next iteration)
					lc = [[sudoku[cntr][cntc] for cntc in range(siz)] for cntr in range(siz)]
					tl = list(sv[rw][cl])
					tl.sort()
					gl.append(SavedStatus(lc,rw,cl,lst.vn+1))
					sudoku[rw][cl] = tl[lst.vn + 1]
					return 1
			else:
				return -1

def Solving():
	global sudoku
	global cols
	global div
	global ccn
	global indeadend
	
	fv = CheckSolutions()
	if ccn == 0:
		indeadend = 0
	else:
		ps = GetPosSol(fv)
		mv = min(min(ps[cnt]) for cnt in range(siz))
		if mv == -1:
			indeadend = 1
	
	if ((ccn == 0 or coherencychecker(sudoku) == True) and indeadend == 0):
		a = SimpleSolution(fv)
		if a == 0:
			a = 2*IntermediateSolution(fv)
			if a == 0:
				sv = EliminateSolutions(fv)
				a = 4*SimpleSolution(sv)
				if a == 0:
					a = 8*IntermediateSolution(sv)
					if a == 0:
						a = 16*GuessManager(sv)
						ccn = 1
	
	#If the current guess has brought to an incoherent status, do not waste loops on it
	else:
		sv = EliminateSolutions(fv)
		a = 16*GuessManager(sv)
	
	return a


#get data transfer from inputs in GUI (indirectly)
def startnew(tpl):
	global siz
	global div
	global srow
	global scol
	global posnum
	global sudoku
	global slvdsudoku
	
	siz = tpl[0]
	srow = tpl[1]
	scol = tpl[2]
	div = [tpl[1], tpl[2]]
	posnum = {i + 1 for i in range(siz)}
	sudoku = [[0 for _ in range(siz)] for _ in range(siz)]
	slvdsudoku =  [[0 for _ in range(siz)] for _ in range(siz)]
	createfinal(tpl[4])
	
	return siz, srow, scol, sudoku, slvdsudoku


def generatefull():
	global siz
	global div
	global posnum
	global sudoku
	global slvdsudoku
	
	allsdks = list()
	csdk = [[0 for _ in range(siz)] for _ in range(siz)]
	shcp = list()
	blanktrgt = siz**2 - siz*2 - 1
	blankcnt = siz**2
	
	while blankcnt > blanktrgt:
		#Fill a new cell with a random number
		csdk[random.randint(0,siz-1)][random.randint(0,siz-1)] = random.randint(1,siz)
		if coherencychecker(csdk):
			shcp = [[csdk[i][j] for j in range(siz)] for i in range(siz)]
			allsdks.append(shcp)
			blankcnt = blankcntr(csdk)
		else:
			csdk = [[(allsdks[-1])[i][j] for j in range(siz)] for i in range(siz)]
	sudoku = [[allsdks[-1][i][j] for j in range(siz)] for i in range(siz)]
	
	while blankcntr(sudoku) > 0 or coherencychecker(sudoku) == False:
		if Solving() < 0:
			return False
	
	slvdsudoku = [[sudoku[i][j] for j in range(siz)] for i in range(siz)]
	return True


def createfinal(diff):
	global siz
	global scol
	global srow
	global div
	global posnum
	global sudoku
	global slvdsudoku
	
	tmp = False
	while tmp == False:
		tmp = generatefull()
	
	minblanks = siz**2 * 0.5 - 1
	allsdks = list()
	csdk = [[sudoku[i][j] for j in range(siz)] for i in range(siz)]
	dlvl = 0
	
	#Create a sudoku with a given, relatively small number of blank cells quickly (without checks at every loop)
	while dlvl != 1:
		dlvl = 0
		sudoku = [[slvdsudoku[i][j] for j in range(siz)] for i in range(siz)]
		while blankcntr(sudoku) < minblanks:
			sudoku[random.randint(0,siz-1)][random.randint(0,siz-1)] = 0
		csdk = [[sudoku[i][j] for j in range(siz)] for i in range(siz)]
		while blankcntr(sudoku) > 0 or coherencychecker(sudoku) == False:
			dlvl = max(dlvl, Solving())
	
	allsdks.append(csdk)
	dlvls = [1]
	cnt = 0
	
	#Eliminate further values one by one, with complicated checks
	while cnt < siz**2:
		cnt += 1
		cdiff = 1
		sudoku = [[allsdks[-1][i][j] for j in range(siz)] for i in range(siz)]
		sudoku[random.randint(0,siz-1)][random.randint(0,siz-1)] = 0
		csdk = [[sudoku[i][j] for j in range(siz)] for i in range(siz)]
		while blankcntr(sudoku) > 0 or coherencychecker(sudoku) == False:
			cdiff = max(cdiff, Solving())
		#Handle case brute force is required and this is requested by user
		if diff == 3 and cdiff == 16:
			sudoku = [[csdk[i][j] for j in range(siz)] for i in range(siz)]
			break
		#Handle case hard sudoku is requested and this is the current level
		elif diff == 2 and (cdiff == 4 or cdiff == 8):
			sudoku = [[csdk[i][j] for j in range(siz)] for i in range(siz)]
			break
		#Handle case target difficulty level is not exceeded
		elif 2**diff >= cdiff:
			allsdks.append(csdk)
			dlvls.append(cdiff)
		#Handle case target difficulty level is exceeded
		else:
			#Handle case target difficulty level has already been reached
			if dlvls[-1] == 2**diff:
				sudoku = [[csdk[i][j] for j in range(siz)] for i in range(siz)]
				break
			#Handle case target difficulty level has not been reached yet
			else:
				dlvls.pop()
	#Case "hard" or "extreme" sudoku can not be reached - avoid infinite loop and absence of outcome
	else:
		sudoku = [[allsdks[-1][i][j] for j in range(siz)] for i in range(siz)]