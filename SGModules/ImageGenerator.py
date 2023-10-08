import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import os.path

siz = 9
div = [3,3]
canvsize = 750
sdksize = 660
sudoku = list()
slvdsudoku = list()

#get data transfer from inputs in GUI (indirectly)
def getdata(tpl):
	global siz
	global div
	global sudoku
	global slvdsudoku
	
	siz = tpl[0]
	div = [tpl[1], tpl[2]]
	sudoku = tpl[3]
	slvdsudoku = tpl[4]


def creategrid():
	global siz
	global div
	global canvsize
	global sdksize
	
	grd = PIL.Image.new(mode = "RGB", size = (canvsize, canvsize), color = (255,255,255))
	drwl = PIL.ImageDraw.Draw(grd)
	
	offs = (canvsize - sdksize) * 0.5
	dst = int(sdksize/siz)
	
	#create vertical lines
	for i in range(siz+1):
		if i % div[0] == 0:
			drwl.line([offs + i*dst, offs, offs + i*dst, offs + siz * dst], width = 3, fill = (0,0,0))
		else:
			drwl.line([offs + i*dst, offs, offs + i*dst, offs + siz * dst], width = 1, fill = (0,0,0))
	
	#create horizontal lines
	for i in range(siz+1):
		if i % div[1] == 0:
			drwl.line([offs, offs + i*dst, offs + siz * dst, offs + i*dst], width = 3, fill = (0,0,0))
		else:
			drwl.line([offs, offs + i*dst, offs + siz * dst, offs + i*dst], width = 1, fill = (0,0,0))
	
	#grd.save("grid.jpg")
	return grd


def getnames():
	i = 1
	while True:
		if os.path.exists(f"EmptySudoku_{i}.jpg") and os.path.exists(f"FilledSudoku_{i}.jpg") and os.path.exists(f"WithSolutionSudoku_{i}.jpg"):
			i += 1
			continue
		return f"EmptySudoku_{i}.jpg", f"FilledSudoku_{i}.jpg", f"WithSolutionSudoku_{i}.jpg"


def exporttoimg(tpl):
	global siz
	global div
	global canvsize
	global sdksize
	global sudoku
	global slvdsudoku
	
	getdata(tpl)
	sdkimg = creategrid()
	slvdimg = sdkimg.copy()
	nms = getnames()
	myfnt = PIL.ImageFont.truetype("arial.ttf",int((sdksize/siz)*0.66))
	sdkime = PIL.ImageDraw.Draw(sdkimg)
	slvdime = PIL.ImageDraw.Draw(slvdimg)
	offs = (canvsize - sdksize) * 0.5
	dst = int(sdksize/siz)
	
	#Iterate through the sudoku, if the given cell is blank in the sudoku, put it in red into the solved one, otherwise put it in black into both
	for i in range(siz):
		for j in range(siz):
			if sudoku[i][j] == 0:
				slvdime.text((offs + int((j + 0.2) * dst), offs + int((i + 0.2) * dst)), str(slvdsudoku[i][j]), fill = (255,0,0), font = myfnt)
			else:
				slvdime.text((offs + int((j + 0.2) * dst), offs + int((i + 0.2) * dst)), str(slvdsudoku[i][j]), fill = (0,0,0), font = myfnt)
				sdkime.text((offs + int((j + 0.2) * dst), offs + int((i + 0.2) * dst)), str(slvdsudoku[i][j]), fill = (0,0,0), font = myfnt)
	
	sdkimg.save(nms[0])
	slvdimg.save(nms[1])
	
	collated = PIL.Image.new(mode = "RGB", size = (canvsize * 2, canvsize), color = (255,255,255))
	collated.paste(sdkimg, (0,0))
	collated.paste(slvdimg, (canvsize, 0))
	collated.save(nms[2])