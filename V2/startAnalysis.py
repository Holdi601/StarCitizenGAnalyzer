import sys
import cv2
import ctypes
import os
import glob
import re
import platform
from datetime import date
from easyocr import Reader
import statistics
import ctypes
import time

Debug=True
user32 = ctypes.windll.user32
def Mbox(title, text, style):
	return ctypes.windll.user32.MessageBoxW(0, text, title, style)

pathParts = sys.argv[0].split('\\') #Windows if you want it for linux do it yourself :P
DataOutput= pathParts[0]
for i in range(1,len(pathParts)-1):
	DataOutput=DataOutput+'\\'+pathParts[i]
DataOutput = DataOutput+'\\DataOutput\\'
if not os.path.exists(DataOutput):
	os.makedirs(DataOutput) 

SpaceShip = 'Debug-Debug-Debug'
Short = True
if len(sys.argv)>1:
	SpaceShip=sys.argv[1]
	valShort = float(sys.argv[2])
	if valShort < 0:
		Short=False
	else:
		Short=True
else:
	SpaceShip="Aegis-Vanguard_Sentinel-NR_MC"
SpaceShip =  SpaceShip.replace(',','')


HalfHeight = int(user32.GetSystemMetrics(1)/2)
HalfWidth = int(user32.GetSystemMetrics(0)/2)
print(HalfHeight)
print(HalfWidth)

class Direction:
	def __init__(self):
		self.fwd=-1.0
		self.aft=-1.0
		self.up=-1.0
		self.down=-1.0
		self.left=-1.0
		self.right=-1.0
		self.fwdup=-1.0
		self.fwddown=-1.0
		self.fwdleft=-1.0
		self.fwdright=-1.0
		self.fwdupleft=-1.0
		self.fwdupright=-1.0
		self.fwddownleft=-1.0
		self.fwddownright=-1.0
		self.aftup=-1.0
		self.aftdown=-1.0
		self.aftleft=-1.0
		self.aftright=-1.0
		self.aftupleft=-1.0
		self.aftupright=-1.0
		self.aftdownleft=-1.0
		self.aftdownright=-1.0
		self.downleft=-1.0
		self.downright=-1.0
		self.upleft=-1.0
		self.upright=-1.0

def dts(dict):
		result=""
		for key in dict:
			result=result+";"+str(key)+";"+str(dict[key])
		return result[1:]
	
def cleanArray(arr):
	result=[]
	lastValue = arr[0]
	result.append(lastValue)
	for i in range(1, len(arr)):
		if arr[i]<0:
			result.append(lastValue)
		else:
			result.append(arr[i])
		lastValue=arr[i]
	return result
		



def writeShipResults(prefix, filewriter, NormAcc, BurnAcc, BurnTime, CDTime, HBTime):
	filewriter.write(prefix+","+str(NormAcc.fwd)			+","+str(BurnAcc.fwd)			+","+str(BurnTime.fwd)			+","+str(CDTime.fwd)			+","+str(HBTime.fwd)				+",fwd,none,none\n")
	filewriter.write(prefix+","+str(NormAcc.aft)			+","+str(BurnAcc.aft)			+","+str(BurnTime.aft)			+","+str(CDTime.aft)			+","+str(HBTime.aft)				+",aft,none,none\n")
	filewriter.write(prefix+","+str(NormAcc.left)			+","+str(BurnAcc.left)			+","+str(BurnTime.left)			+","+str(CDTime.left)			+","+str(HBTime.left)				+",none,none,left\n")
	filewriter.write(prefix+","+str(NormAcc.right)			+","+str(BurnAcc.right)			+","+str(BurnTime.right)		+","+str(CDTime.right)			+","+str(HBTime.right)				+",none,none,right\n")
	filewriter.write(prefix+","+str(NormAcc.up)				+","+str(BurnAcc.up)			+","+str(BurnTime.up)			+","+str(CDTime.up)				+","+str(HBTime.up)					+",none,up,none\n")
	filewriter.write(prefix+","+str(NormAcc.down)			+","+str(BurnAcc.down)			+","+str(BurnTime.down)			+","+str(CDTime.down)			+","+str(HBTime.down)				+",none,down,none\n")
	filewriter.write(prefix+","+str(NormAcc.fwdup)			+","+str(BurnAcc.fwdup)			+","+str(BurnTime.fwdup)		+","+str(CDTime.fwdup)			+","+str(HBTime.fwdup)				+",fwd,up,none\n")
	filewriter.write(prefix+","+str(NormAcc.fwddown)		+","+str(BurnAcc.fwddown)		+","+str(BurnTime.fwddown)		+","+str(CDTime.fwddown)		+","+str(HBTime.fwddown)			+",fwd,down,none\n")
	filewriter.write(prefix+","+str(NormAcc.fwdleft)		+","+str(BurnAcc.fwdleft)		+","+str(BurnTime.fwdleft)		+","+str(CDTime.fwdleft)		+","+str(HBTime.fwdleft)			+",fwd,none,left\n")
	filewriter.write(prefix+","+str(NormAcc.fwdright)		+","+str(BurnAcc.fwdright)		+","+str(BurnTime.fwdright)		+","+str(CDTime.fwdright)		+","+str(HBTime.fwdright)			+",fwd,none,right\n")
	filewriter.write(prefix+","+str(NormAcc.fwdupleft)		+","+str(BurnAcc.fwdupleft)		+","+str(BurnTime.fwdupleft)	+","+str(CDTime.fwdupleft)		+","+str(HBTime.fwdupleft)			+",fwd,up,left\n")
	filewriter.write(prefix+","+str(NormAcc.fwdupright)		+","+str(BurnAcc.fwdupright)	+","+str(BurnTime.fwdupright)	+","+str(CDTime.fwdupright)		+","+str(HBTime.fwdupright)			+",fwd,up,right\n")
	filewriter.write(prefix+","+str(NormAcc.fwddownleft)	+","+str(BurnAcc.fwddownleft)	+","+str(BurnTime.fwddownleft)	+","+str(CDTime.fwddownleft)	+","+str(HBTime.fwddownleft)		+",fwd,down,left\n")
	filewriter.write(prefix+","+str(NormAcc.fwddownright)	+","+str(BurnAcc.fwddownright)	+","+str(BurnTime.fwddownright)	+","+str(CDTime.fwddownright)	+","+str(HBTime.fwddownright)		+",fwd,down,right\n")
	filewriter.write(prefix+","+str(NormAcc.aftup)			+","+str(BurnAcc.aftup)			+","+str(BurnTime.aftup)		+","+str(CDTime.aftup)			+","+str(HBTime.aftup)				+",aft,up,none\n")
	filewriter.write(prefix+","+str(NormAcc.aftdown)		+","+str(BurnAcc.aftdown)		+","+str(BurnTime.aftdown)		+","+str(CDTime.aftdown)		+","+str(HBTime.aftdown)			+",aft,down,none\n")
	filewriter.write(prefix+","+str(NormAcc.aftleft)		+","+str(BurnAcc.aftleft)		+","+str(BurnTime.aftleft)		+","+str(CDTime.aftleft)		+","+str(HBTime.aftleft)			+",aft,none,left\n")
	filewriter.write(prefix+","+str(NormAcc.aftright)		+","+str(BurnAcc.aftright)		+","+str(BurnTime.aftright)		+","+str(CDTime.aftright)		+","+str(HBTime.aftright)			+",aft,none,right\n")
	filewriter.write(prefix+","+str(NormAcc.aftupleft)		+","+str(BurnAcc.aftupleft)		+","+str(BurnTime.aftupleft)	+","+str(CDTime.aftupleft)		+","+str(HBTime.aftupleft)			+",aft,up,left\n")
	filewriter.write(prefix+","+str(NormAcc.aftupright)		+","+str(BurnAcc.aftupright)	+","+str(BurnTime.aftupright)	+","+str(CDTime.aftupright)		+","+str(HBTime.aftupright)			+",aft,up,right\n")
	filewriter.write(prefix+","+str(NormAcc.aftdownleft)	+","+str(BurnAcc.aftdownleft)	+","+str(BurnTime.aftdownleft)	+","+str(CDTime.aftdownleft)	+","+str(HBTime.aftdownleft)		+",aft,down,left\n")
	filewriter.write(prefix+","+str(NormAcc.aftdownright)	+","+str(BurnAcc.aftdownright)	+","+str(BurnTime.aftdownright)	+","+str(CDTime.aftdownright)	+","+str(HBTime.aftdownright)		+",aft,down,right\n")
	filewriter.write(prefix+","+str(NormAcc.downleft)		+","+str(BurnAcc.downleft)		+","+str(BurnTime.downleft)		+","+str(CDTime.downleft)		+","+str(HBTime.downleft)			+",none,down,left\n")
	filewriter.write(prefix+","+str(NormAcc.downright)		+","+str(BurnAcc.downright)		+","+str(BurnTime.downright)	+","+str(CDTime.downright)		+","+str(HBTime.downright)			+",none,down,right\n")
	filewriter.write(prefix+","+str(NormAcc.upleft)			+","+str(BurnAcc.upleft)		+","+str(BurnTime.upleft)		+","+str(CDTime.upleft)			+","+str(HBTime.upleft)				+",none,up,left\n")
	filewriter.write(prefix+","+str(NormAcc.upright)		+","+str(BurnAcc.upright)		+","+str(BurnTime.upright)		+","+str(CDTime.upright)		+","+str(HBTime.upright)			+",none,up,right\n")



class ShipResults:
	def __init__(self):
		self.NormalAcceleration= Direction()
		self.BurnerAcceleration= Direction()
		self.BurnTime = Direction()
		self.CoolTime = Direction()
		self.HeatedBurnTime = Direction()
		self.TestDate=""
		self.Name=""
		
	def writeResults(self, path, append=False):
		outputFile = None
		completePath = path+"\\"+self.Name+"_overview"+".stats"
		outputFileTL = None
		completePathTL = path+"\\"+self.Name+"_timeLine"+".stats"
		if append:
			outputFile=open(completePath, "a")
			outputFileTL=open(completePathTL, "a")
		else:
			outputFile=open(completePath, "w")
			outputFileTL=open(completePathTL, "w")
		Manufacteur=""
		Model=""
		Comment=""
		parts = self.Name.split('-')
		if len(parts)>0:
			Manufacteur=parts[0]
			if len(parts)>1:
				Model=parts[1]
				if len(parts)>2:
					Comment=parts[2]
		pre=Manufacteur+","+Model+","+Comment+","+self.TestDate
		writeShipResults(pre, outputFile, self.NormalAcceleration, self.BurnerAcceleration, self.BurnTime, self.CoolTime, self.HeatedBurnTime)
		outputFile.close()
		startPart=Manufacteur+","+Model+","+Comment+","+self.TestDate
		buStartup=startPart
		startPart=buStartup+",raw"
		if not Short:
			writeTimeGraph(startPart, outputFileTL, self.TimeGraph)
			print("now clean")
			startPart=buStartup+",cleaned"
			writeTimeGraph(startPart, outputFileTL, self.TimeGraph.getCleanObject())
		outputFileTL.close()


def createDummyDirection():
	f1=Direction()
	f1.fwd=1.0
	f1.aft=2.0
	f1.up=3.0
	f1.down=4.0
	f1.left=5.0
	f1.right=6.0
	f1.fwdup=7.0
	f1.fwddown=8.0
	f1.fwdleft=9.0
	f1.fwdright=10.0
	f1.fwdupleft=11.0
	f1.fwdupright=12.0
	f1.fwddownleft=21.0
	f1.fwddownright=-31.0
	f1.aftup=41.0
	f1.aftdown=51.0
	f1.aftleft=61.0
	f1.aftright=71.0
	f1.aftupleft=81.0
	f1.aftupright=91.0
	f1.aftdownleft=101.0
	f1.aftdownright=111.0
	f1.downleft=-121.0
	f1.downright=131.0
	f1.upleft=141.0
	f1.upright=161.0
	return f1
	
def createDummyArray():
	arr=[]
	for i in range(0,100):
		arr.append(i)
	return arr
	
def createDummyBT():
	f1 = BurnTimeGraph()
	f1.fwd=createDummyArray()
	f1.aft=createDummyArray()
	f1.up=createDummyArray()
	f1.down=createDummyArray()
	f1.left=createDummyArray()
	f1.right=createDummyArray()
	f1.fwdup=createDummyArray()
	f1.fwddown=createDummyArray()
	f1.fwdleft=createDummyArray()
	f1.fwdright=createDummyArray()
	f1.fwdupleft=createDummyArray()
	f1.fwdupright=createDummyArray()
	f1.fwddownleft=createDummyArray()
	f1.fwddownright=createDummyArray()
	f1.aftup=createDummyArray()
	f1.aftdown=createDummyArray()
	f1.aftleft=createDummyArray()
	f1.aftright=createDummyArray()
	f1.aftupleft=createDummyArray()
	f1.aftupright=createDummyArray()
	f1.aftdownleft=createDummyArray()
	f1.aftdownright=createDummyArray()
	f1.downleft=createDummyArray()
	f1.downright=createDummyArray()
	f1.upleft=createDummyArray()
	f1.upright=createDummyArray()
	return f1
	
def ShipWriteUnitTest():
	r = ShipResults()
	r.NormalAcceleration=createDummyDirection()
	r.BurnerAcceleration=createDummyDirection()
	r.BurnTime = createDummyDirection()
	r.CoolTime = createDummyDirection()
	r.HeatedBurnTime = createDummyDirection()
	r.TimeGraph = createDummyBT()
	r.writeResults("F:\\Dropbox\\Programmierung\\StarCitizenGAnalyzer\\DataOutput\\")
	

#ShipWriteUnitTest()

def TranslatePercentageOffCenterToPixel(Percentage, HoW):
	dimensionToDealWith=0
	if HoW =="h":
		dimensionToDealWith=HalfHeight
	else:
		dimensionToDealWith=HalfWidth
	if Percentage >=100:
		return dimensionToDealWith
	elif Percentage<=0:
		return 0
	else:
		return int(float(dimensionToDealWith)*float(Percentage/100.0))

gYper = 25
YwidPer = 50
gYpix = HalfHeight-TranslatePercentageOffCenterToPixel(gYper,'h')
gYoff = gYpix+TranslatePercentageOffCenterToPixel(YwidPer,'h')
gXper = 25
XwidPer = 50
gXpix = HalfWidth-TranslatePercentageOffCenterToPixel(gXper,'w')
gXoff = gXpix+TranslatePercentageOffCenterToPixel(XwidPer,'w')

cap= cv2.VideoCapture(0)
testStage = 1
failuresInRow = 0
succesesInRow = 0
noAccsInRow = 0
AccsInRow =0
frameCounter = 0
results = ShipResults()
results.Name = SpaceShip
today = date.today()
results.TestDate=today.strftime("%Y-%m-%d")
stats = {}
currentFrame=0

def get_most_appearing_val(stats):
	returnVal = -1.0
	appearances = -1
	for val in stats:
		if stats[val] > appearances:
			appearances=stats[val]
			returnVal=val
	return returnVal
	


def analyze_results_from_section_acceleration(section, stats):
	if section==0:
		return
	elif section==1:
		results.NormalAcceleration.fwd=get_most_appearing_val(stats)
		print("Normal Acceleration Forward max Acceleration G detected: "+str(results.NormalAcceleration.fwd))
	elif section==2:
		results.NormalAcceleration.aft=get_most_appearing_val(stats)
		print("Normal Acceleration Aft max Acceleration G detected: "+str(results.NormalAcceleration.aft))
	elif section==3:
		results.NormalAcceleration.left=get_most_appearing_val(stats)
		print("Normal Acceleration Left max Acceleration G detected: "+str(results.NormalAcceleration.left))
	elif section==4:
		results.NormalAcceleration.right=get_most_appearing_val(stats)
		print("Normal Acceleration Right max Acceleration G detected: "+str(results.NormalAcceleration.right))
	elif section==5:
		results.NormalAcceleration.up=get_most_appearing_val(stats)
		print("Normal Acceleration Up max Acceleration G detected: "+str(results.NormalAcceleration.up))
	elif section==6:
		results.NormalAcceleration.down=get_most_appearing_val(stats)
		print("Normal Acceleration Down max Acceleration G detected: "+str(results.NormalAcceleration.down))
	elif section==7:
		results.NormalAcceleration.fwdup=get_most_appearing_val(stats)
		print("Burner Acceleration fwdup max Acceleration G detected: "+str(results.NormalAcceleration.fwdup))
	elif section==8:
		results.NormalAcceleration.fwddown=get_most_appearing_val(stats)
		print("Burner Acceleration fwddown max Acceleration G detected: "+str(results.NormalAcceleration.fwddown))
	elif section==9:
		results.NormalAcceleration.fwdleft=get_most_appearing_val(stats)
		print("Burner Acceleration fwdleft max Acceleration G detected: "+str(results.NormalAcceleration.fwdleft))
	elif section==10:
		results.NormalAcceleration.fwdright=get_most_appearing_val(stats)
		print("Burner Acceleration fwdright max Acceleration G detected: "+str(results.NormalAcceleration.fwdright))
	elif section==11:
		results.NormalAcceleration.fwdupleft=get_most_appearing_val(stats)
		print("Burner Acceleration fwdupleft max Acceleration G detected: "+str(results.NormalAcceleration.fwdupleft))
	elif section==12:
		results.NormalAcceleration.fwdupright=get_most_appearing_val(stats)
		print("Burner Acceleration fwdupright max Acceleration G detected: "+str(results.NormalAcceleration.fwdupright))
	elif section==13:
		results.NormalAcceleration.fwddownleft=get_most_appearing_val(stats)
		print("Burner Acceleration fwddownleft max Acceleration G detected: "+str(results.NormalAcceleration.fwddownleft))
	elif section==14:
		results.NormalAcceleration.fwddownright=get_most_appearing_val(stats)
		print("Burner Acceleration fwddownright max Acceleration G detected: "+str(results.NormalAcceleration.fwddownright))
	elif section==15:
		results.NormalAcceleration.aftup=get_most_appearing_val(stats)
		print("Burner Acceleration aftup max Acceleration G detected: "+str(results.NormalAcceleration.aftup))
	elif section==16:
		results.NormalAcceleration.aftdown=get_most_appearing_val(stats)
		print("Burner Acceleration aftdown max Acceleration G detected: "+str(results.NormalAcceleration.aftdown))
	elif section==17:
		results.NormalAcceleration.aftleft=get_most_appearing_val(stats)
		print("Burner Acceleration aftleft max Acceleration G detected: "+str(results.NormalAcceleration.aftleft))
	elif section==18:
		results.NormalAcceleration.aftright=get_most_appearing_val(stats)
		print("Burner Acceleration aftright max Acceleration G detected: "+str(results.NormalAcceleration.aftright))
	elif section==19:
		results.NormalAcceleration.aftupleft=get_most_appearing_val(stats)
		print("Burner Acceleration aftupleft max Acceleration G detected: "+str(results.NormalAcceleration.aftupleft))
	elif section==20:
		results.NormalAcceleration.aftupright=get_most_appearing_val(stats)
		print("Burner Acceleration aftupright max Acceleration G detected: "+str(results.NormalAcceleration.aftupright))
	elif section==21:
		results.NormalAcceleration.aftdownleft=get_most_appearing_val(stats)
		print("Burner Acceleration aftdownleft max Acceleration G detected: "+str(results.NormalAcceleration.aftdownleft))
	elif section==22:
		results.NormalAcceleration.aftdownright=get_most_appearing_val(stats)
		print("Burner Acceleration aftdownright max Acceleration G detected: "+str(results.NormalAcceleration.aftdownright))
	elif section==23:
		results.NormalAcceleration.downleft=get_most_appearing_val(stats)
		print("Burner Acceleration downleft max Acceleration G detected: "+str(results.NormalAcceleration.downleft))
	elif section==24:
		results.NormalAcceleration.downright=get_most_appearing_val(stats)
		print("Burner Acceleration downright max Acceleration G detected: "+str(results.NormalAcceleration.downright))
	elif section==25:
		results.NormalAcceleration.upleft=get_most_appearing_val(stats)
		print("Burner Acceleration upleft max Acceleration G detected: "+str(results.NormalAcceleration.upleft))
	elif section==26:
		results.NormalAcceleration.upright=get_most_appearing_val(stats)
		print("Burner Acceleration upright max Acceleration G detected: "+str(results.NormalAcceleration.upright))
	elif section==27:
		results.BurnerAcceleration.fwd=get_most_appearing_val(stats)
		print("Normal Acceleration Forward max Acceleration G detected: "+str(results.BurnerAcceleration.fwd))
	elif section==28:
		results.BurnerAcceleration.aft=get_most_appearing_val(stats)
		print("Normal Acceleration Aft max Acceleration G detected: "+str(results.BurnerAcceleration.aft))
	elif section==29:
		results.BurnerAcceleration.left=get_most_appearing_val(stats)
		print("Normal Acceleration Left max Acceleration G detected: "+str(results.BurnerAcceleration.left))
	elif section==30:
		results.BurnerAcceleration.right=get_most_appearing_val(stats)
		print("Normal Acceleration Right max Acceleration G detected: "+str(results.BurnerAcceleration.right))
	elif section==31:
		results.BurnerAcceleration.up=get_most_appearing_val(stats)
		print("Normal Acceleration Up max Acceleration G detected: "+str(results.BurnerAcceleration.up))
	elif section==32:
		results.BurnerAcceleration.down=get_most_appearing_val(stats)
		print("Normal Acceleration Down max Acceleration G detected: "+str(results.BurnerAcceleration.down))
	elif section==33:
		results.BurnerAcceleration.fwdup=get_most_appearing_val(stats)
		print("Burner Acceleration fwdup max Acceleration G detected: "+str(results.BurnerAcceleration.fwdup))
	elif section==34:
		results.BurnerAcceleration.fwddown=get_most_appearing_val(stats)
		print("Burner Acceleration fwddown max Acceleration G detected: "+str(results.BurnerAcceleration.fwddown))
	elif section==35:
		results.BurnerAcceleration.fwdleft=get_most_appearing_val(stats)
		print("Burner Acceleration fwdleft max Acceleration G detected: "+str(results.BurnerAcceleration.fwdleft))
	elif section==36:
		results.BurnerAcceleration.fwdright=get_most_appearing_val(stats)
		print("Burner Acceleration fwdright max Acceleration G detected: "+str(results.BurnerAcceleration.fwdright))
	elif section==37:
		results.BurnerAcceleration.fwdupleft=get_most_appearing_val(stats)
		print("Burner Acceleration fwdupleft max Acceleration G detected: "+str(results.BurnerAcceleration.fwdupleft))
	elif section==38:
		results.BurnerAcceleration.fwdupright=get_most_appearing_val(stats)
		print("Burner Acceleration fwdupright max Acceleration G detected: "+str(results.BurnerAcceleration.fwdupright))
	elif section==39:
		results.BurnerAcceleration.fwddownleft=get_most_appearing_val(stats)
		print("Burner Acceleration fwddownleft max Acceleration G detected: "+str(results.BurnerAcceleration.fwddownleft))
	elif section==40:
		results.BurnerAcceleration.fwddownright=get_most_appearing_val(stats)
		print("Burner Acceleration fwddownright max Acceleration G detected: "+str(results.BurnerAcceleration.fwddownright))
	elif section==41:
		results.BurnerAcceleration.aftup=get_most_appearing_val(stats)
		print("Burner Acceleration aftup max Acceleration G detected: "+str(results.BurnerAcceleration.aftup))
	elif section==42:
		results.BurnerAcceleration.aftdown=get_most_appearing_val(stats)
		print("Burner Acceleration aftdown max Acceleration G detected: "+str(results.BurnerAcceleration.aftdown))
	elif section==43:
		results.BurnerAcceleration.aftleft=get_most_appearing_val(stats)
		print("Burner Acceleration aftleft max Acceleration G detected: "+str(results.BurnerAcceleration.aftleft))
	elif section==44:
		results.BurnerAcceleration.aftright=get_most_appearing_val(stats)
		print("Burner Acceleration aftright max Acceleration G detected: "+str(results.BurnerAcceleration.aftright))
	elif section==45:
		results.BurnerAcceleration.aftupleft=get_most_appearing_val(stats)
		print("Burner Acceleration aftupleft max Acceleration G detected: "+str(results.BurnerAcceleration.aftupleft))
	elif section==46:
		results.BurnerAcceleration.aftupright=get_most_appearing_val(stats)
		print("Burner Acceleration aftupright max Acceleration G detected: "+str(results.BurnerAcceleration.aftupright))
	elif section==47:
		results.BurnerAcceleration.aftdownleft=get_most_appearing_val(stats)
		print("Burner Acceleration aftdownleft max Acceleration G detected: "+str(results.BurnerAcceleration.aftdownleft))
	elif section==48:
		results.BurnerAcceleration.aftdownright=get_most_appearing_val(stats)
		print("Burner Acceleration aftdownright max Acceleration G detected: "+str(results.BurnerAcceleration.aftdownright))
	elif section==49:
		results.BurnerAcceleration.downleft=get_most_appearing_val(stats)
		print("Burner Acceleration downleft max Acceleration G detected: "+str(results.BurnerAcceleration.downleft))
	elif section==50:
		results.BurnerAcceleration.downright=get_most_appearing_val(stats)
		print("Burner Acceleration downright max Acceleration G detected: "+str(results.BurnerAcceleration.downright))
	elif section==51:
		results.BurnerAcceleration.upleft=get_most_appearing_val(stats)
		print("Burner Acceleration upleft max Acceleration G detected: "+str(results.BurnerAcceleration.upleft))
	elif section==52:
		results.BurnerAcceleration.upright=get_most_appearing_val(stats)
		print("Burner Acceleration upright max Acceleration G detected: "+str(results.BurnerAcceleration.upright))


rdr = Reader(['en'],gpu=True)

xTracker = []
yTracker = []

gXref=35
gXoff=63
gYref=371
gYoff=50
oXHeat=gXref+233
oXHoff=100
oYHeat=gYref-265
oYoff=50

GEARdetect = False
LOCKdetect = False

def sample_size(stats):
	result=0
	for key in stats:
		result+=stats[key]
	return result

while cap.isOpened():
	st =  time.process_time()
	currentFrame+=1
	ret, frame = cap.read()
	if frame is None:
		break;
	txresults=[]
	Gmeter= frame[gYref:gYref+gYoff, gXref:gXref+gXoff]
	oheat = frame[oYHeat:oYHeat+oYoff, oXHeat:oXHeat+oXHoff]
	try:
		txresults= rdr.readtext(Gmeter)
	except:
		print("Failed read screen " + str(currentFrame))
	
	
	GreadOut=-1.0
	if len(txresults)>0:
		for elements in txresults:
			if len(elements)>1:
				textFound=elements[1]
				match = re.search("(\d|[o]|[O]|[g]|[s]|[S]|[I]|[i]|[l])*(\d|[o]|[O]|[g]|[s]|[S]|[I]|[i]|[l])[.](\d|[o]|[O]|[g]|[s]|[S]|[I]|[i]|[l])", textFound)
				if match:
					strToUse = match[0].replace('o','0').replace('O','0').replace('g','9').replace('s','5').replace('S','5').replace('i','1').replace('I','1').replace('l','1')
					GreadOut=float(strToUse)
					break
	if Debug:
		cv2.imshow('SCAnalyze', Gmeter)
		cv2.imshow('Heated', oheat)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	nd =  time.process_time()
	print(nd-st)


cap.release()
cv2.destroyAllWindows

results.writeResults(DataOutput)
print("Done")

