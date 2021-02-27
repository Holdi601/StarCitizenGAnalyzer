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
if len(sys.argv)>1:
	SpaceShip=sys.argv[1]
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
		
	def toCsvString(self):
		result=str(self.fwd)+","+str(self.aft)+","+str(self.left)+","+str(self.right)+","+str(self.up)+","+str(self.down)
		return result

def dts(dict):
		result=""
		for key in dict:
			result=result+";"+str(key)+";"+str(dict[key])
		return result[1:]
		
class BurnTimeGraph:
	def __init__(self):
		self.fwd=[]
		self.aft=[]
		self.up=[]
		self.down=[]
		self.left=[]
		self.right=[]
		
class BurnTimeDirection:
	def __init__(self):
		self.fwd={}
		self.aft={}
		self.up={}
		self.down={}
		self.left={}
		self.right={}
		
	
	def toCsvString(self):
		result=dts(self.fwd)+","+dts(self.aft)+","+dts(self.left)+","+dts(self.right)+","+dts(self.up)+","+dts(self.down)
		return result

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
		
	def writeResults(self, path, append=True):
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
		resultLine=Manufacteur+","+Model+","+Comment+","+self.TestDate+","+self.NormalAcceleration.toCsvString()+","+self.BurnerAcceleration.toCsvString()+","+self.BurnTime.toCsvString()+","+self.CoolTime.toCsvString()+","+self.HeatedBurnTime.toCsvString()+"\n"
		outputFile.write(resultLine)
		outputFile.close()
		startPart=Manufacteur+","+Model+","+Comment+","+self.TestDate
		for i in range(0, len(self.TimeGraph.fwd)):
			lineToWrite=startPart+",fwd,"+str(i+1)+","+str(self.TimeGraph.fwd[i])+"\n"
			outputFileTL.write(lineToWrite)
		for i in range(0, len(self.TimeGraph.aft)):
			lineToWrite=startPart+",aft,"+str(i+1)+","+str(self.TimeGraph.aft[i])+"\n"
			outputFileTL.write(lineToWrite)
		for i in range(0, len(self.TimeGraph.left)):
			lineToWrite=startPart+",left,"+str(i+1)+","+str(self.TimeGraph.left[i])+"\n"
			outputFileTL.write(lineToWrite)
		for i in range(0, len(self.TimeGraph.right)):
			lineToWrite=startPart+",right,"+str(i+1)+","+str(self.TimeGraph.right[i])+"\n"
			outputFileTL.write(lineToWrite)
		for i in range(0, len(self.TimeGraph.up)):
			lineToWrite=startPart+",up,"+str(i+1)+","+str(self.TimeGraph.up[i])+"\n"
			outputFileTL.write(lineToWrite)
		for i in range(0, len(self.TimeGraph.down)):
			lineToWrite=startPart+",down,"+str(i+1)+","+str(self.TimeGraph.down[i])+"\n"
			outputFileTL.write(lineToWrite)
		outputFileTL.close()


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
YwidPer = 45
gYpix = HalfHeight+TranslatePercentageOffCenterToPixel(gYper,'h')
gYoff = TranslatePercentageOffCenterToPixel(YwidPer,'h')
gXper = 50
XwidPer = 20
gXpix = HalfWidth-TranslatePercentageOffCenterToPixel(gXper,'w')
gXoff = TranslatePercentageOffCenterToPixel(XwidPer,'w')

cap= cv2.VideoCapture(LatestVideo)
testStage = 0
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
framesToStartSection=5
framesToDeclareNoAcc=35
framesToDeclareAcc=35
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
	if section==13:
		results.TimeGraph.fwd = graph
	if section==14:
		results.TimeGraph.aft = graph
	if section==15:
		results.TimeGraph.left = graph
	if section==16:
		results.TimeGraph.right = graph
	if section==17:
		results.TimeGraph.up = graph
	if section==18:
		results.TimeGraph.down = graph
	

def analyze_results_from_time(section, burnstage, frames):
	if section==13:
		if burnerStage==0:
			results.BurnTime.fwd=frames*TPF
		elif burnerStage==1:
			results.CoolTime.fwd=frames*TPF
		else:
			results.HeatedBurnTime.fwd=frames*TPF
			accelerationToBeAbove=results.NormalAcceleration.aft-0.1
	elif section==14:
		if burnerStage==0:
			results.BurnTime.aft=frames*TPF
		elif burnerStage==1:
			results.CoolTime.aft=frames*TPF
		else:
			results.HeatedBurnTime.aft=frames*TPF
			accelerationToBeAbove=results.NormalAcceleration.left-0.1
	elif section==15:
		if burnerStage==0:
			results.BurnTime.left=frames*TPF
		elif burnerStage==1:
			results.CoolTime.left=frames*TPF
		else:
			results.HeatedBurnTime.left=frames*TPF
			accelerationToBeAbove=results.NormalAcceleration.right-0.1
	elif section==16:
		if burnerStage==0:
			results.BurnTime.right=frames*TPF
		elif burnerStage==1:
			results.CoolTime.right=frames*TPF
		else:
			results.HeatedBurnTime.right=frames*TPF
			accelerationToBeAbove=results.NormalAcceleration.up-0.1
	elif section==17:
		if burnerStage==0:
			results.BurnTime.up=frames*TPF
		elif burnerStage==1:
			results.CoolTime.up=frames*TPF
		else:
			results.HeatedBurnTime.up=frames*TPF
			accelerationToBeAbove=results.NormalAcceleration.down-0.1
	elif section==18:
		if burnerStage==0:
			results.BurnTime.down=frames*TPF
		elif burnerStage==1:
			results.CoolTime.down=frames*TPF
		else:
			results.HeatedBurnTime.down=frames*TPF
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
		results.BurnerAcceleration.fwd=get_most_appearing_val(stats)
		print("Burner Acceleration Forward max Acceleration G detected: "+str(results.BurnerAcceleration.fwd))
	elif section==8:
		results.BurnerAcceleration.aft=get_most_appearing_val(stats)
		print("Burner Acceleration Aft max Acceleration G detected: "+str(results.BurnerAcceleration.aft))
	elif section==9:
		results.BurnerAcceleration.left=get_most_appearing_val(stats)
		print("Burner Acceleration Left max Acceleration G detected: "+str(results.BurnerAcceleration.left))
	elif section==10:
		results.BurnerAcceleration.right=get_most_appearing_val(stats)
		print("Burner Acceleration Right max Acceleration G detected: "+str(results.BurnerAcceleration.right))
	elif section==11:
		results.BurnerAcceleration.up=get_most_appearing_val(stats)
		print("Burner Acceleration Up max Acceleration G detected: "+str(results.BurnerAcceleration.up))
	elif section==12:
		results.BurnerAcceleration.down=get_most_appearing_val(stats)
		accelerationToBeAbove=results.NormalAcceleration.fwd-0.1
		print("Burner Acceleration Down max Acceleration G detected: "+str(results.BurnerAcceleration.down))

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
rdr = Reader(['en'],gpu=True)
previousAcc=[]
GreadsToSave=60
burnerActive=False
while cap.isOpened():
	currentFrame+=1
	ret, frame = cap.read()
	if frame is None:
		break;
	if currentFrame >0:
		Gmeter= frame[gYpix:gYpix+gYoff, gXpix:gXpix+gXoff]
		Gmeter=cv2.cvtColor(Gmeter, cv2.COLOR_BGR2GRAY)
		Gmeter=apply_brightness_contrast(Gmeter,0, 128)
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
					match = re.search("(\d|[o]|[O]|[g])*(\d|[o]|[O]|[g])[.](\d|[o]|[O]|[g])", textFound)
					if match:
						strToUse = match[0].replace('o','0').replace('O','0').replace('g','9')
						GreadOut=float(strToUse)
						break
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
					if testStage>12 and not burnerActive:
						burnerActive=True
				if GreadOut in stats:
					stats[GreadOut]+=1
				else:
					stats[GreadOut]=1					
			else:
				noAccsInRow+=1
				AccsInRow=0
		elif failuresInRow==framesToCloseSection:
			succesesInRow=0
			print(str(testStage) + ' Section Closed Section Duration in Frames: '+ str(lastLegitFrame-referenceFrame))
			print(stats)
			if testStage<13:
				analyze_results_from_section_acceleration(testStage, stats)
			else:
				framesToCloseSection=int(CoolDownPeriodInFrames)
			stats={}
			closed=True
			TimeLine=[]
		if testStage>12 and burnerActive:
			if GreadOut>=0:
				TimeLine.append(GreadOut)
			else:
				TimeLine.append(previousAcc[0])
		if succesesInRow==framesToStartSection and closed:
			print('Section Started')
			closed=False
			referenceFrame=currentFrame-(framesToStartSection-1)
			testStage+=1
			burnerStage=0
			referenceStartAcc=-1
			noAccsInRow=0
			AccsInRow=0
			referenceStartAcc=-1
			referenceNoAcc=-1
				
		if noAccsInRow== framesToDeclareNoAcc and testStage>12 and referenceStartAcc>=0 and burnerStage==0:
			framesOfAcc = currentFrame-framesToDeclareNoAcc-referenceStartAcc
			analyze_results_from_time(testStage, burnerStage, framesOfAcc)
			referenceStartAcc=-1
			burnerStage+=1
			referenceNoAcc=currentFrame-framesToDeclareNoAcc
			succesesInRow=-1
			stats={}
		elif burnerStage==1 and  referenceNoAcc>0 and testStage>12 and AccsInRow==framesToDeclareAcc:
			framesOfCD=currentFrame-framesToDeclareAcc-referenceNoAcc
			analyze_results_from_time(testStage, burnerStage, framesOfCD)
			burnerStage+=1
			referenceNoAcc=-1
			referenceStartAcc=currentFrame-framesToDeclareAcc
			stats={}
		elif burnerStage==2 and referenceStartAcc>0 and testStage>12 and noAccsInRow== framesToDeclareNoAcc:
			framesOfAcc = currentFrame-framesToDeclareNoAcc-referenceStartAcc
			analyze_results_from_time(testStage, burnerStage, framesOfAcc)
			analyze_graph(testStage, TimeLine)
			burnerStage+=1
			stats={}
			TimeLine=[]
			print("Done in direction, waiting for external view")
		cv2.imshow('SCAnalyze', Gmeter)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

cap.release()
cv2.destroyAllWindows

results.writeResults(DataOutput)
print("Done")

