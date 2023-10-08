import SGModules.SGGUI as gi
import SGModules.GeneratorEngine as ge
import SGModules.ImageGenerator as ig

def main():
	while True:
		#Give the user the possibility to set the inputs
		while True:
			gi.wupdate()
			#Generate button presssed and request is feasible
			if gi.requestqueried() == True:
				if gi.checkfeasibility() == True:
					gi.wupdate()
					break
		
		#Create the requested amount of blank sudokus and convert them to image
		datagot = gi.forwarddata()
		for i in range(datagot[3]):
			gensdk = ge.startnew(datagot)
			ig.exporttoimg(gensdk)
		gi.readymsg()

main()
