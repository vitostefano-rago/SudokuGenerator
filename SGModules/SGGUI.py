import tkinter as tk


#variables
mws = 500
bs = 1
mystyle = ("Arial", 20)
btnstyle = ("Arial", 15)
ssiz = 9
srow = 3
scol = 3
snum = 1
LEVELS = ["  Easy", "Medium", "  Hard", "  Evil"]
clevel = LEVELS[0]
STATUSES = ["     Waiting", "     Working", "      Ready!", "Wrong input!!"]
cstatus = STATUSES[0]
requestgiven = False


#Functions
def sizincr():
	global ssiz
	ssiz += 1
	lbl_sza1["text"] = str(ssiz)
	if ssiz < 10:
		lbl_sza1.place(x = 350, y = 12)
	else:
		lbl_sza1.place(x = 340, y = 12)

def sizdecr():
	global ssiz
	if ssiz > 6:
		ssiz -= 1
		lbl_sza1["text"] = str(ssiz)
	if ssiz < 10:
		lbl_sza1.place(x = 350, y = 12)
	else:
		lbl_sza1.place(x = 340, y = 12)

def rnincr():
	global srow
	srow += 1
	lbl_sza2["text"] = str(srow)

def rndecr():
	global srow
	if srow > 2:
		srow -= 1
		lbl_sza2["text"] = str(srow)

def cnincr():
	global scol
	scol += 1
	lbl_sza3["text"] = str(scol)

def cndecr():
	global scol
	if scol > 2:
		scol -= 1
		lbl_sza3["text"] = str(scol)

def nrincr():
	global snum
	snum += 1
	lbl_qa["text"] = str(snum)

def nrdecr():
	global snum
	if snum > 1:
		snum -= 1
		lbl_qa["text"] = str(snum)

def lvlincr():
	global LEVELS
	global clevel
	if LEVELS.index(clevel) != len(LEVELS) - 1:
		clevel = LEVELS[LEVELS.index(clevel) + 1]
		lbl_lvla["text"] = clevel

def lvldecr():
	global LEVELS
	global clevel
	if LEVELS.index(clevel) != 0:
		clevel = LEVELS[LEVELS.index(clevel) - 1]
		lbl_lvla["text"] = clevel

def checkfeasibility():
	global ssiz
	global srow
	global scol
	global STATUSES
	global cstatus
	
	if ssiz == srow * scol:
		cstatus = STATUSES[1]
		lbl_sts["text"] = cstatus
		lbl_sts["fg"] = "black"
		return True
	
	else:
		cstatus = STATUSES[-1]
		lbl_sts["text"] = cstatus
		lbl_sts["fg"] = "red"
		return False

def startpressed():
	global requestgiven
	requestgiven = True

def requestqueried():
	global requestgiven
	tmp = requestgiven
	requestgiven = False
	return tmp

def forwarddata():
	global ssiz
	global srow
	global scol
	global snum
	global LEVELS
	global clevel
	
	return ssiz, srow, scol, snum, LEVELS.index(clevel)

def readymsg():
	global STATUSES
	global cstatus
	
	cstatus = STATUSES[-2]
	lbl_sts["text"] = cstatus
	window.update()

def wupdate():
	window.update()


#Main window
window = tk.Tk()
window.title("Sudoku Generator")
window.minsize(mws, mws)
window.maxsize(mws, mws)
canvas = tk.Canvas(master = window, width = mws, height = mws)
canvas.pack()


#Labels
lbl_szq1 = tk.Label(master = window, text = "Set grid size", font = mystyle)
lbl_szq1.place(x = 25, y = 12)
lbl_szq2 = tk.Label(master = window, text = "Set row size", font = mystyle)
lbl_szq2.place(x = 25, y = 72)
lbl_szq3 = tk.Label(master = window, text = "Set column size", font = mystyle)
lbl_szq3.place(x = 25, y = 132)
lbl_lvlq = tk.Label(master = window, text = "Set difficulty", font = mystyle)
lbl_lvlq.place(x = 25, y = 192)
lbl_qq = tk.Label(master = window, text = "Set number of desired Sudokus", font = mystyle)
lbl_qq.place(x = 55, y = 252)
lbl_sza1 = tk.Label(master = window, text = str(ssiz), font = mystyle)
lbl_sza1.place(x = 350, y = 12)
lbl_sza2 = tk.Label(master = window, text = str(srow), font = mystyle)
lbl_sza2.place(x = 350, y = 72)
lbl_sza3 = tk.Label(master = window, text = str(scol), font = mystyle)
lbl_sza3.place(x = 350, y = 132)
lbl_lvla = tk.Label(master = window, text = clevel, font = mystyle)
lbl_lvla.place(x = 310, y = 192)
lbl_qa = tk.Label(master = window, text = str(snum), font = mystyle)
lbl_qa.place(x = 240, y = 300)
lbl_sts = tk.Label(master = window, text = cstatus, font = mystyle)
lbl_sts.place(x = 160, y = 450)


#Grids
canvas.create_line(5, 5, 5, mws - 5, width = 2)
canvas.create_line(5, mws - 5, mws - 5, mws - 5, width = 2)
canvas.create_line(mws - 5, mws - 5, mws - 5, 5, width = 2)
canvas.create_line(mws - 5, 5, 5, 5, width = 2)
canvas.create_line(5, 60, mws - 5, 60, width = 2)
canvas.create_line(5, 120, mws - 5, 120, width = 2)
canvas.create_line(5, 180, mws - 5, 180, width = 2)
canvas.create_line(5, 240, mws - 5, 240, width = 2)
canvas.create_line(5, 350, mws - 5, 350, width = 2)
canvas.create_line(5, 435, mws - 5, 435, width = 2)


#Buttons
btn_sizincr = tk.Button(text = " + ", font = btnstyle, width = 2, height = 1, command = sizincr)
btn_sizincr.place(x = 400, y = 12)
btn_sizdecr = tk.Button(text = " - ", font = btnstyle, width = 2, height = 1, command = sizdecr)
btn_sizdecr.place(x = 290, y = 12)
btn_rnincr = tk.Button(text = " + ", font = btnstyle, width = 2, height = 1, command = rnincr)
btn_rnincr.place(x = 400, y = 72)
btn_rndecr = tk.Button(text = " - ", font = btnstyle, width = 2, height = 1, command = rndecr)
btn_rndecr.place(x = 290, y = 72)
btn_cnincr = tk.Button(text = " + ", font = btnstyle, width = 2, height = 1, command = cnincr)
btn_cnincr.place(x = 400, y = 132)
btn_cndecr = tk.Button(text = " - ", font = btnstyle, width = 2, height = 1, command = cndecr)
btn_cndecr.place(x = 290, y = 132)
btn_lvlincr = tk.Button(text = " + ", font = btnstyle, width = 2, height = 1, command = lvlincr)
btn_lvlincr.place(x = 450, y = 192)
btn_lvldecr = tk.Button(text = " - ", font = btnstyle, width = 2, height = 1, command = lvldecr)
btn_lvldecr.place(x = 240, y = 192)
btn_nrincr = tk.Button(text = " + ", font = btnstyle, width = 2, height = 1, command = nrincr)
btn_nrincr.place(x = 290, y = 300)
btn_nrdecr = tk.Button(text = " - ", font = btnstyle, width = 2, height = 1, command = nrdecr)
btn_nrdecr.place(x = 180, y = 300)
btn_strt = tk.Button(text = "  Generate!  ", font = mystyle, command = startpressed)
btn_strt.place(x = 160, y = 365)