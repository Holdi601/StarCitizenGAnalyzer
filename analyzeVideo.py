import sys
import cv2
import ctypes
import os
import glob
import pytesseract
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
	
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

VideoFilePath = 'Y:\\Records\\Squadron 42 - Star Citizen\\'
LatestVideo = GetYoungestVideoInFoler(VideoFilePath)
SpaceShip = 'Debug-Debug-Debug'
if len(sys.argv)>1:
	SpaceShip=sys.argv[1]
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

class ShipResults:
	def __init__(self):
		self.NormalAcceleration= Direction()
		self.BurnerAcceleration= Direction()
		self.BurnTime = Direction()
		self.CoolTime = Direction()
		self.HeatedBurnTime = Direction()
		self.TestDate=""
		self.Name=""

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
YwidPer = 15
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
frameCounter = 0
results = ShipResults()
results.Name = SpaceShip
results.TestDate=testDate
stats = {}
currentFrame=0
referenceFrame =-1
referenceTestFrame = -1
lastLegitFrame =-1
lastFrameAbove =-1
framesToCloseSection=55
framesToStartSection=5
CoolDownPeriodInSeconds=9
CoolDownPeriodInFrames=(1000/TPF)*CoolDownPeriodInSeconds

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

while cap.isOpened():
	currentFrame+=1
	ret, frame = cap.read()
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
		else:
			failuresInRow=0
		if GreadOut>=0.0:
			succesesInRow+=1
			lastLegitFrame=currentFrame
			if GreadOut>0.0:
				lastFrameAbove=currentFrame
				if GreadOut in stats:
					stats[GreadOut]+=1
				else:
					stats[GreadOut]=1
		elif failuresInRow==framesToCloseSection:
			succesesInRow=0
			print(str(testStage) + ' Section Closed Section Duration in Frames: '+ str(lastLegitFrame-referenceFrame))
			print(stats)
			if testStage<13:
				analyze_results_from_section_acceleration(testStage, stats)
			else:
				framesToCloseSection=CoolDownPeriodInFrames
			stats={}
			closed=True
		if succesesInRow==framesToStartSection and closed:
			print('Section Started')
			closed=False
			referenceFrame=currentFrame-(framesToStartSection-1)
			testStage+=1
		cv2.imshow('SCAnalyze', Gmeter)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

cap.release()
cv2.destroyAllWindows
print(stats)

