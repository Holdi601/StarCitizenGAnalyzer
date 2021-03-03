import sys
import cv2
import ctypes
import os
import glob
from videoprops import get_video_properties
import re
import platform
from datetime import datetime
from easyocr import Reader
import statistics

Debug=True
def Mbox(title, text, style):
	return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def GetYoungestVideoInFoler(path):
	files = os.listdir(path)
	paths = [os.path.join(path, basename) for basename in files]
	return max(paths, key=os.path.getctime)
	
pathParts = sys.argv[0].split('\\') #Windows if you want it for linux do it yourself :P
DataOutput= pathParts[0]
for i in range(1,len(pathParts)-1):
	DataOutput=DataOutput+'\\'+pathParts[i]
DataOutput = DataOutput+'\\DataOutput\\'
if not os.path.exists(DataOutput):
	os.makedirs(DataOutput) 
VideoFilePath = 'Y:\\Records\\Squadron 42 - Star Citizen\\'
LatestVideo = GetYoungestVideoInFoler(VideoFilePath)
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
	SpaceShip="Aegis-Gladius_Pirate-NR_MC"
SpaceShip =  SpaceShip.replace(',','')
videoProperties= get_video_properties(LatestVideo)
HalfHeight = int(videoProperties['height']/2)
HalfWidth = int(videoProperties['width']/2)
FPS_str = videoProperties['avg_frame_rate'].split('/')
TPF = (1.0/(float(FPS_str[0])/float(FPS_str[1])))*1000
ts = int(os.path.getmtime(LatestVideo))
testDate = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')

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
		
class BurnTimeGraph:
	def __init__(self):
		self.fwd=[]
		self.aft=[]
		self.up=[]
		self.down=[]
		self.left=[]
		self.right=[]
		self.fwdup=[]
		self.fwddown=[]
		self.fwdleft=[]
		self.fwdright=[]
		self.fwdupleft=[]
		self.fwdupright=[]
		self.fwddownleft=[]
		self.fwddownright=[]
		self.aftup=[]
		self.aftdown=[]
		self.aftleft=[]
		self.aftright=[]
		self.aftupleft=[]
		self.aftupright=[]
		self.aftdownleft=[]
		self.aftdownright=[]
		self.downleft=[]
		self.downright=[]
		self.upleft=[]
		self.upright=[]
		
	def getCleanObject(self):
		Btresult = BurnTimeGraph()
		Btresult.fwd = cleanArray(self.fwd)
		Btresult.aft = cleanArray(self.aft)
		Btresult.up = cleanArray(self.up)
		Btresult.down = cleanArray(self.down)
		Btresult.left = cleanArray(self.left)
		Btresult.right = cleanArray(self.right)
		Btresult.fwdup = cleanArray(self.fwdup)
		Btresult.fwddown = cleanArray(self.fwddown)
		Btresult.fwdleft = cleanArray(self.fwdleft)
		Btresult.fwdright = cleanArray(self.fwdright)
		Btresult.fwdupleft = cleanArray(self.fwdupleft)
		Btresult.fwdupright = cleanArray(self.fwdupright)
		Btresult.fwddownleft = cleanArray(self.fwddownleft)
		Btresult.fwddownright = cleanArray(self.fwddownright)
		Btresult.aftup = cleanArray(self.aftup)
		Btresult.aftdown = cleanArray(self.aftdown)
		Btresult.aftleft = cleanArray(self.aftleft)
		Btresult.aftright = cleanArray(self.aftright)
		Btresult.aftupleft = cleanArray(self.aftupleft)
		Btresult.aftupright = cleanArray(self.aftupright)
		Btresult.aftdownleft = cleanArray(self.aftdownleft)
		Btresult.aftdownright = cleanArray(self.aftdownright)
		Btresult.downleft = cleanArray(self.downleft)
		Btresult.downright = cleanArray(self.downright)
		Btresult.upleft = cleanArray(self.upleft)
		Btresult.upright = cleanArray(self.upright)
		return Btresult

def writeArrayToFile( prefix, fileWriter, arr, dir1, dir2, dir3):
	for i in range(0, len(arr)):
			lineToWrite=prefix+","+dir1+","+dir2+","+dir3+","+str(i+1)+","+str(arr[i])+"\n"
			fileWriter.write(lineToWrite)

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

def writeTimeGraph(prefix, filewriter, tg):
	writeArrayToFile(prefix, filewriter, tg.fwd, "fwd","none","none")
	writeArrayToFile(prefix, filewriter, tg.aft, "aft","none","none")
	writeArrayToFile(prefix, filewriter, tg.left, "none","none","left")
	writeArrayToFile(prefix, filewriter, tg.right, "none","none","right")
	writeArrayToFile(prefix, filewriter, tg.up, "none","up","none")
	writeArrayToFile(prefix, filewriter, tg.down, "none","down","none")
	writeArrayToFile(prefix, filewriter, tg.fwdup, "fwd","up","none")
	writeArrayToFile(prefix, filewriter, tg.fwddown, "fwd","down","none")
	writeArrayToFile(prefix, filewriter, tg.fwdleft, "fwd","none","left")
	writeArrayToFile(prefix, filewriter, tg.fwdright, "fwd","none","right")
	writeArrayToFile(prefix, filewriter, tg.fwdupleft, "fwd","up","left")
	writeArrayToFile(prefix, filewriter, tg.fwdupright, "fwd","up","right")
	writeArrayToFile(prefix, filewriter, tg.fwddownleft, "fwd","down","left")
	writeArrayToFile(prefix, filewriter, tg.fwddownright, "fwd","down","right")
	writeArrayToFile(prefix, filewriter, tg.aftup, "aft","up","none")
	writeArrayToFile(prefix, filewriter, tg.aftdown, "aft","down","none")
	writeArrayToFile(prefix, filewriter, tg.aftleft, "aft","none","left")
	writeArrayToFile(prefix, filewriter, tg.aftright, "aft","none","right")
	writeArrayToFile(prefix, filewriter, tg.aftupleft, "aft","up","left")
	writeArrayToFile(prefix, filewriter, tg.aftupright, "aft","up","right")
	writeArrayToFile(prefix, filewriter, tg.aftdownleft, "aft","down","left")
	writeArrayToFile(prefix, filewriter, tg.aftdownright, "aft","down","right")
	writeArrayToFile(prefix, filewriter, tg.downleft, "none","down","left")
	writeArrayToFile(prefix, filewriter, tg.downright, "none","down","right")
	writeArrayToFile(prefix, filewriter, tg.upleft, "none","up","left")
	writeArrayToFile(prefix, filewriter, tg.upright, "none","up","right")

class ShipResults:
	def __init__(self):
		self.NormalAcceleration= Direction()
		self.BurnerAcceleration= Direction()
		self.BurnTime = Direction()
		self.CoolTime = Direction()
		self.HeatedBurnTime = Direction()
		self.TimeGraph = BurnTimeGraph()
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

gYper = 16
YwidPer = 47
gYpix = HalfHeight+TranslatePercentageOffCenterToPixel(gYper,'h')
gYoff = gYpix+TranslatePercentageOffCenterToPixel(YwidPer,'h')
gXper = 50
XwidPer = 28
gXpix = HalfWidth-TranslatePercentageOffCenterToPixel(gXper,'w')
gXoff = gXpix+TranslatePercentageOffCenterToPixel(XwidPer,'w')

cap= cv2.VideoCapture(LatestVideo)
testStage = 1
failuresInRow = 0
succesesInRow = 0
noAccsInRow = 0
AccsInRow =0
frameCounter = 0
results = ShipResults()
results.Name = SpaceShip
results.TestDate=testDate
stats = {}
currentFrame=0
referenceFrame =-1
referenceTestFrame = -1
referenceStartAcc= -1
referenceNoAcc = -1
lastLegitFrame =-1
lastFrameAbove =-1
framesToCloseSection=55
framesToStartSection=15
framesToDeclareNoAcc=6
framesToDeclareAcc=12
CoolDownPeriodInSeconds=9
CoolDownPeriodInFrames=(1000/TPF)*CoolDownPeriodInSeconds
burnerStage=0
accelerationToBeAbove=0.0
TimeLine=[]

def get_most_appearing_val(stats):
	returnVal = -1.0
	appearances = -1
	for val in stats:
		if stats[val] > appearances:
			appearances=stats[val]
			returnVal=val
	return returnVal
	
def analyze_graph(section, graph):
	if section==testStageBurnThreshhold+1:
		results.TimeGraph.fwd = graph
	elif section==testStageBurnThreshhold+2:
		results.TimeGraph.aft = graph
	elif section==testStageBurnThreshhold+3:
		results.TimeGraph.left = graph
	elif section==testStageBurnThreshhold+4:
		results.TimeGraph.right = graph
	elif section==testStageBurnThreshhold+5:
		results.TimeGraph.up = graph
	elif section==testStageBurnThreshhold+6:
		results.TimeGraph.down = graph
	elif section==testStageBurnThreshhold+7:
		results.TimeGraph.fwdup = graph
	elif section==testStageBurnThreshhold+8:
		results.TimeGraph.fwddown = graph
	elif section==testStageBurnThreshhold+9:
		results.TimeGraph.fwdleft = graph
	elif section==testStageBurnThreshhold+10:
		results.TimeGraph.fwdright = graph
	elif section==testStageBurnThreshhold+11:
		results.TimeGraph.fwdupleft = graph
	elif section==testStageBurnThreshhold+12:
		results.TimeGraph.fwdupright = graph
	elif section==testStageBurnThreshhold+13:
		results.TimeGraph.fwddownleft = graph
	elif section==testStageBurnThreshhold+14:
		results.TimeGraph.fwddownright = graph
	elif section==testStageBurnThreshhold+15:
		results.TimeGraph.aftup = graph
	elif section==testStageBurnThreshhold+16:
		results.TimeGraph.aftdown = graph
	elif section==testStageBurnThreshhold+17:
		results.TimeGraph.aftleft = graph
	elif section==testStageBurnThreshhold+18:
		results.TimeGraph.aftright = graph
	elif section==testStageBurnThreshhold+19:
		results.TimeGraph.aftupleft = graph
	elif section==testStageBurnThreshhold+20:
		results.TimeGraph.aftupright = graph
	elif section==testStageBurnThreshhold+21:
		results.TimeGraph.aftdownleft = graph
	elif section==testStageBurnThreshhold+22:
		results.TimeGraph.aftdownright = graph
	elif section==testStageBurnThreshhold+23:
		results.TimeGraph.downleft = graph
	elif section==testStageBurnThreshhold+24:
		results.TimeGraph.downright = graph
	elif section==testStageBurnThreshhold+25:
		results.TimeGraph.upleft = graph
	elif section==testStageBurnThreshhold+26:
		results.TimeGraph.upright = graph
	

def analyze_results_from_time(section, burnstage, frames):
	if section==testStageBurnThreshhold+1:
		if burnerStage==0:
			results.BurnTime.fwd=frames*TPF
		elif burnerStage==1:
			results.CoolTime.fwd=frames*TPF
		else:
			results.HeatedBurnTime.fwd=frames*TPF
	elif section==testStageBurnThreshhold+2:
		if burnerStage==0:
			results.BurnTime.aft=frames*TPF
		elif burnerStage==1:
			results.CoolTime.aft=frames*TPF
		else:
			results.HeatedBurnTime.aft=frames*TPF
	elif section==testStageBurnThreshhold+3:
		if burnerStage==0:
			results.BurnTime.left=frames*TPF
		elif burnerStage==1:
			results.CoolTime.left=frames*TPF
		else:
			results.HeatedBurnTime.left=frames*TPF
	elif section==testStageBurnThreshhold+4:
		if burnerStage==0:
			results.BurnTime.right=frames*TPF
		elif burnerStage==1:
			results.CoolTime.right=frames*TPF
		else:
			results.HeatedBurnTime.right=frames*TPF
	elif section==testStageBurnThreshhold+5:
		if burnerStage==0:
			results.BurnTime.up=frames*TPF
		elif burnerStage==1:
			results.CoolTime.up=frames*TPF
		else:
			results.HeatedBurnTime.up=frames*TPF
	elif section==testStageBurnThreshhold+6:
		if burnerStage==0:
			results.BurnTime.down=frames*TPF
		elif burnerStage==1:
			results.CoolTime.down=frames*TPF
		else:
			results.HeatedBurnTime.down=frames*TPF
	elif section==testStageBurnThreshhold+7:
		if burnerStage==0:
			results.BurnTime.fwdup=frames*TPF
		elif burnerStage==1:
			results.CoolTime.fwdup=frames*TPF
		else:
			results.HeatedBurnTime.fwdup=frames*TPF
	elif section==testStageBurnThreshhold+8:
		if burnerStage==0:
			results.BurnTime.fwddown=frames*TPF
		elif burnerStage==1:
			results.CoolTime.fwddown=frames*TPF
		else:
			results.HeatedBurnTime.fwddown=frames*TPF
	elif section==testStageBurnThreshhold+9:
		if burnerStage==0:
			results.BurnTime.fwdleft=frames*TPF
		elif burnerStage==1:
			results.CoolTime.fwdleft=frames*TPF
		else:
			results.HeatedBurnTime.fwdleft=frames*TPF
	elif section==testStageBurnThreshhold+10:
		if burnerStage==0:
			results.BurnTime.fwdright=frames*TPF
		elif burnerStage==1:
			results.CoolTime.fwdright=frames*TPF
		else:
			results.HeatedBurnTime.fwdright=frames*TPF
	elif section==testStageBurnThreshhold+11:
		if burnerStage==0:
			results.BurnTime.fwdupleft=frames*TPF
		elif burnerStage==1:
			results.CoolTime.fwdupleft=frames*TPF
		else:
			results.HeatedBurnTime.fwdupleft=frames*TPF
	elif section==testStageBurnThreshhold+12:
		if burnerStage==0:
			results.BurnTime.fwdupright=frames*TPF
		elif burnerStage==1:
			results.CoolTime.fwdupright=frames*TPF
		else:
			results.HeatedBurnTime.fwdupright=frames*TPF
	elif section==testStageBurnThreshhold+13:
		if burnerStage==0:
			results.BurnTime.fwddownleft=frames*TPF
		elif burnerStage==1:
			results.CoolTime.fwddownleft=frames*TPF
		else:
			results.HeatedBurnTime.fwddownleft=frames*TPF
	elif section==testStageBurnThreshhold+14:
		if burnerStage==0:
			results.BurnTime.fwddownright=frames*TPF
		elif burnerStage==1:
			results.CoolTime.fwddownright=frames*TPF
		else:
			results.HeatedBurnTime.fwddownright=frames*TPF
	elif section==testStageBurnThreshhold+15:
		if burnerStage==0:
			results.BurnTime.aftup=frames*TPF
		elif burnerStage==1:
			results.CoolTime.aftup=frames*TPF
		else:
			results.HeatedBurnTime.aftup=frames*TPF
	elif section==testStageBurnThreshhold+16:
		if burnerStage==0:
			results.BurnTime.aftdown=frames*TPF
		elif burnerStage==1:
			results.CoolTime.aftdown=frames*TPF
		else:
			results.HeatedBurnTime.aftdown=frames*TPF
	elif section==testStageBurnThreshhold+17:
		if burnerStage==0:
			results.BurnTime.aftleft=frames*TPF
		elif burnerStage==1:
			results.CoolTime.aftleft=frames*TPF
		else:
			results.HeatedBurnTime.aftleft=frames*TPF
	elif section==testStageBurnThreshhold+18:
		if burnerStage==0:
			results.BurnTime.aftright=frames*TPF
		elif burnerStage==1:
			results.CoolTime.aftright=frames*TPF
		else:
			results.HeatedBurnTime.aftright=frames*TPF
	elif section==testStageBurnThreshhold+19:
		if burnerStage==0:
			results.BurnTime.aftupleft=frames*TPF
		elif burnerStage==1:
			results.CoolTime.aftupleft=frames*TPF
		else:
			results.HeatedBurnTime.aftupleft=frames*TPF
	elif section==testStageBurnThreshhold+20:
		if burnerStage==0:
			results.BurnTime.aftupright=frames*TPF
		elif burnerStage==1:
			results.CoolTime.aftupright=frames*TPF
		else:
			results.HeatedBurnTime.aftupright=frames*TPF
	elif section==testStageBurnThreshhold+21:
		if burnerStage==0:
			results.BurnTime.aftdownleft=frames*TPF
		elif burnerStage==1:
			results.CoolTime.aftdownleft=frames*TPF
		else:
			results.HeatedBurnTime.aftdownleft=frames*TPF
	elif section==testStageBurnThreshhold+22:
		if burnerStage==0:
			results.BurnTime.aftdownright=frames*TPF
		elif burnerStage==1:
			results.CoolTime.aftdownright=frames*TPF
		else:
			results.HeatedBurnTime.aftdownright=frames*TPF
	elif section==testStageBurnThreshhold+23:
		if burnerStage==0:
			results.BurnTime.downleft=frames*TPF
		elif burnerStage==1:
			results.CoolTime.downleft=frames*TPF
		else:
			results.HeatedBurnTime.downleft=frames*TPF
	elif section==testStageBurnThreshhold+24:
		if burnerStage==0:
			results.BurnTime.downright=frames*TPF
		elif burnerStage==1:
			results.CoolTime.downright=frames*TPF
		else:
			results.HeatedBurnTime.downright=frames*TPF
	elif section==testStageBurnThreshhold+25:
		if burnerStage==0:
			results.BurnTime.upleft=frames*TPF
		elif burnerStage==1:
			results.CoolTime.upleft=frames*TPF
		else:
			results.HeatedBurnTime.upleft=frames*TPF
	elif section==testStageBurnThreshhold+26:
		if burnerStage==0:
			results.BurnTime.upright=frames*TPF
		elif burnerStage==1:
			results.CoolTime.upright=frames*TPF
		else:
			results.HeatedBurnTime.upright=frames*TPF
	print(str(section)+" "+ str(burnerStage) +" finished with " + str(frames*TPF))

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

def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):
	if brightness != 0:
		if brightness > 0:
			shadow = brightness
			highlight = 255
		else:
			shadow = 0
			highlight = 255 + brightness
		alpha_b = (highlight - shadow)/255
		gamma_b = shadow
		buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
	else:
		buf = input_img.copy()
	if contrast != 0:
		f = 131*(contrast + 127)/(127*(131-contrast))
		alpha_c = f
		gamma_c = 127*(1-f)
		buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
	return buf
closed=False
started=False
rdr = Reader(['en'],gpu=True)
previousAcc=[]
GreadsToSave=60
burnerActive=False
TrackerTimer =4.0
TrackerFrame = int((1000/TPF)*TrackerTimer)
FramesToScanTarget = 10
xTracker = []
yTracker = []
BurnerTimeToleranceSeconds = 3
BurnerPressPeriodInSeconds =30- BurnerTimeToleranceSeconds
BurnerPressPeriodInFrames =(1000/TPF)*BurnerPressPeriodInSeconds
BurnerStartRef = -1
testStageBurnThreshhold=52

def sample_size(stats):
	result=0
	for key in stats:
		result+=stats[key]
	return result

while cap.isOpened():
	currentFrame+=1
	ret, frame = cap.read()
	if frame is None:
		break;
	Gmeter=None
	if currentFrame>= TrackerFrame - FramesToScanTarget:
		if currentFrame>TrackerFrame:
			Gmeter= frame[gYpix:gYoff, gXpix:gXoff]
		else:
			Gmeter=frame
		#Gmeter=cv2.cvtColor(Gmeter, cv2.COLOR_BGR2GRAY)
		#Gmeter=apply_brightness_contrast(Gmeter,0, 128)
		txresults=[]
		try:
			txresults= rdr.readtext(Gmeter)
		except:
			print("Failed read screen " + str(currentFrame))
		textFound=""
		GreadOut=-1.0
		if len(txresults)>0:
			for elements in txresults:
				if len(elements)>1:
					textFound=elements[1]
					if Debug:
						cv2.putText(Gmeter,textFound, (int(elements[0][0][0]) , int(elements[0][0][1])), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255))
					if currentFrame>TrackerFrame:
						match = re.search("(\d|[o]|[O]|[g]|[s]|[S]|[I]|[i]|[l])*(\d|[o]|[O]|[g]|[s]|[S]|[I]|[i]|[l])[.](\d|[o]|[O]|[g]|[s]|[S]|[I]|[i]|[l])", textFound)
						if match:
							strToUse = match[0].replace('o','0').replace('O','0').replace('g','9').replace('s','5').replace('S','5').replace('i','1').replace('I','1').replace('l','1')
							GreadOut=float(strToUse)
							break
					if currentFrame >= TrackerFrame - FramesToScanTarget and currentFrame< TrackerFrame-1:
						if textFound=="GEAR":
							xTracker.append(elements[0][0][0])
							yTracker.append(elements[0][0][1])
					elif currentFrame == TrackerFrame-1:
						xMed= statistics.median(xTracker)
						yMed= statistics.median(yTracker)
						gXpix = int(xMed - TranslatePercentageOffCenterToPixel(18, "w"))
						gXoff = int(gXpix + TranslatePercentageOffCenterToPixel(17, "w"))
						gYpix = int(yMed - TranslatePercentageOffCenterToPixel(17, "h"))
						gYoff = int(gYpix + TranslatePercentageOffCenterToPixel(35, "h"))
		if GreadOut<0:
			failuresInRow+=1
			noAccsInRow+=1
			AccsInRow=0
		else:
			failuresInRow=0
		if GreadOut>=0.0:
			succesesInRow+=1
			lastLegitFrame=currentFrame
			previousAcc.insert(0, GreadOut)
			if len(previousAcc)>GreadsToSave:
				previousAcc.pop(GreadsToSave)
			if GreadOut>0.0:
				lastFrameAbove=currentFrame
				noAccsInRow=0
				AccsInRow+=1
				if referenceStartAcc <0:
					referenceStartAcc=currentFrame
					print("Acceleration started")
					if testStage>testStageBurnThreshhold and not burnerActive:
						burnerActive=True
				if GreadOut in stats:
					stats[GreadOut]+=1
				else:
					stats[GreadOut]=1					
			else:
				noAccsInRow+=1
				AccsInRow=0
		elif failuresInRow==framesToCloseSection and not closed and sample_size(stats)>0 and (testStage<13 or currentFrame>(BurnerStartRef+BurnerPressPeriodInFrames)):
			succesesInRow=0
			print(str(testStage) + ' Section Closed Section Duration in Frames: '+ str(lastLegitFrame-referenceFrame))
			print(stats)
			if testStage<testStageBurnThreshhold+1:
				analyze_results_from_section_acceleration(testStage, stats)
			else:
				framesToCloseSection=int(CoolDownPeriodInFrames)
				analyze_graph(testStage, TimeLine)
				if burnerStage < 3:
					framesOfAcc = currentFrame-framesToCloseSection-referenceFrame
					analyze_results_from_time(testStage, burnerStage, framesOfAcc)
			stats={}
			burnerActive=False
			TimeLine=[]
			closed=True
			burnerActive=False
			BurnerStartRef =-1
			if (testStage==(testStageBurnThreshhold+(testStageBurnThreshhold/2)) and not Short) or (Short and testStage==testStageBurnThreshhold):
				break
		if testStage>testStageBurnThreshhold and burnerActive:
			TimeLine.append(GreadOut)
		if succesesInRow==framesToStartSection and closed:
			print('Section Started')
			TimeLine=[]
			for i in range(0, framesToStartSection):
				TimeLine.insert(0, previousAcc[i])
			closed=False
			referenceFrame=currentFrame-(framesToStartSection-1)
			testStage+=1
			burnerStage=0
			referenceStartAcc=-1
			burnerActive=True
			noAccsInRow=0
			AccsInRow=0
			referenceStartAcc=-1
			referenceNoAcc=-1
			stats={}	
		if noAccsInRow== framesToDeclareNoAcc and testStage>testStageBurnThreshhold and referenceStartAcc>=0 and burnerStage==0:
			framesOfAcc = currentFrame-framesToDeclareNoAcc-referenceStartAcc
			BurnerStartRef = referenceStartAcc
			analyze_results_from_time(testStage, burnerStage, framesOfAcc)
			referenceStartAcc=-1
			burnerStage+=1
			referenceNoAcc=currentFrame-framesToDeclareNoAcc
			succesesInRow=-1
		elif burnerStage==1 and  referenceNoAcc>0 and testStage>testStageBurnThreshhold and AccsInRow==framesToDeclareAcc:
			framesOfCD=currentFrame-framesToDeclareAcc-referenceNoAcc
			analyze_results_from_time(testStage, burnerStage, framesOfCD)
			burnerStage+=1
			referenceNoAcc=-1
			referenceStartAcc=currentFrame-framesToDeclareAcc
		elif burnerStage==2 and referenceStartAcc>0 and testStage>testStageBurnThreshhold and noAccsInRow== framesToDeclareNoAcc:
			framesOfAcc = currentFrame-framesToDeclareNoAcc-referenceStartAcc
			analyze_results_from_time(testStage, burnerStage, framesOfAcc)
			burnerStage+=1
			print("Done in direction, waiting for external view")
		if (testStage==(testStageBurnThreshhold+(testStageBurnThreshhold/2)) and burnerStage==3):
			break
		if Debug:
			cv2.imshow('SCAnalyze', Gmeter)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

framesToCloseSection=int(CoolDownPeriodInFrames)
analyze_graph(testStage, TimeLine)
if burnerStage < 3:
	framesOfAcc = currentFrame-framesToCloseSection-referenceFrame
	analyze_results_from_time(testStage, burnerStage, framesOfAcc)

cap.release()
cv2.destroyAllWindows

results.writeResults(DataOutput)
print("Done")

