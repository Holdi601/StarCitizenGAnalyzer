import os
import sys

AppendSummary = False
pathParts = sys.argv[0].split('\\') #Windows if you want it for linux do it yourself :P
DataPath= pathParts[0]
for i in range(1,len(pathParts)-1):
	DataPath=DataPath+'\\'+pathParts[i]
DataPath = DataPath+'\\DataOutput\\'
print(DataPath)
if not os.path.exists(DataPath):
	os.makedirs(DataPath) 
SummaryPath = DataPath+ "Summary\\"
fileName="summary_overview.csv"
fileWrite=None

tlfileName="summary_timeline.csv"
tlWrite=None

if not os.path.exists(SummaryPath):
	os.makedirs(SummaryPath)

if AppendSummary:
	fileWrite=open(SummaryPath+fileName, "a")
	tlWrite=open(SummaryPath+tlfileName, "a")
else:
	fileWrite=open(SummaryPath+fileName, "w")
	tlWrite=open(SummaryPath+tlfileName, "w")

for file in os.listdir(DataPath):
	if file.endswith("_overview.stats"):
		fileReader = open(os.path.join(DataPath, file),"r")
		fileWrite.write(fileReader.read())
		fileReader.close()
fileWrite.close()

for file in os.listdir(DataPath):
	if file.endswith("_timeLine.stats"):
		fileReader = open(os.path.join(DataPath, file),"r")
		tlWrite.write(fileReader.read())
		fileReader.close()
tlWrite.close()