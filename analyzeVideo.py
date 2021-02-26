import sys
import cv2
import ctypes
import os
import glob
import pytesseract
from videoprops import get_video_properties
import re

def Mbox(title, text, style):
	return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def GetYoungestVideoInFoler(path):
	files = os.listdir(path)
	paths = [os.path.join(path, basename) for basename in files]
	return max(paths, key=os.path.getctime)
	
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

VideoFilePath = 'Y:\\Records\\Squadron 42 - Star Citizen\\'
LatestVideo = GetYoungestVideoInFoler(VideoFilePath)
SpaceShip = ''
if len(sys.argv)>1:
	SpaceShip=sys.argv[1]
videoProperties= get_video_properties(LatestVideo)
HalfHeight = int(videoProperties['height']/2)
HalfWidth = int(videoProperties['width']/2)
FPS_str = videoProperties['avg_frame_rate'].split('/')
TPF = (1.0/(float(FPS_str[0])/float(FPS_str[1])))*1000
print(HalfHeight)
print(HalfWidth)
print(TPF)

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

gYper = 4
YwidPer = 13
gYpix = HalfHeight+TranslatePercentageOffCenterToPixel(gYper,'h')
gYoff = TranslatePercentageOffCenterToPixel(YwidPer,'h')
gXper = 26
XwidPer = 10
gXpix = HalfWidth-TranslatePercentageOffCenterToPixel(gXper,'w')
gXoff = TranslatePercentageOffCenterToPixel(XwidPer,'w')

tYper = 22
tYwidPer = 15
tYpix = HalfHeight-TranslatePercentageOffCenterToPixel(tYper,'h')
tYoff = TranslatePercentageOffCenterToPixel(tYwidPer,'h')
tXper = 30
tXwidPer = 10
tXpix = HalfWidth-TranslatePercentageOffCenterToPixel(tXper,'w')
tXoff = TranslatePercentageOffCenterToPixel(tXwidPer,'w')

cap= cv2.VideoCapture(LatestVideo)
testStage = 0
failuresInRow = 0
frameCounter = 0
results = ShipResults()
stats = {}

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

while cap.isOpened():
	ret, frame = cap.read()
	Gmeter= frame[gYpix:gYpix+gYoff, gXpix:gXpix+gXoff]
	Gmeter=cv2.cvtColor(Gmeter, cv2.COLOR_BGR2GRAY)
	Gmeter=apply_brightness_contrast(Gmeter,0,25)
	GlimiterRawLines=pytesseract.image_to_string(Gmeter).split('\n')
	GreadOut=-1.0
	for poss in GlimiterRawLines:
		match = re.search("(\d|[o]|[O])*(\d|[o]|[O])[.](\d|[o]|[O])", poss)
		if match:
			GreadOut=float(match[0])
	print(GreadOut)
	if GreadOut<0:
		failuresInRow+=1
	else:
		failuresInRow=0
	if GreadOut>0.0:
		if GreadOut in stats:
			stats[GreadOut]+=1
		else:
			stats[GreadOut]=1
	#cv2.imshow('SCAnalyze', Gmeter)
	#if cv2.waitKey(1) & 0xFF == ord('q'):
	#	break

cap.release()
cv2.destroyAllWindows

