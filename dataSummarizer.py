import os
import sys

AppendSummary = True
pathParts = sys.argv[0].split('\\') #Windows if you want it for linux do it yourself :P
DataPath= pathParts[0]
for i in range(1,len(pathParts)-1):
	DataPath=DataPath+'\\'+pathParts[i]
DataPath = DataPath+'\\DataOutput\\'
print(DataPath)
if not os.path.exists(DataPath):
	os.makedirs(DataPath) 
SummaryPath = DataPath+ "Summary\\"
fileName="summary.csv"
fileWrite=None

if not os.path.exists(SummaryPath):
	os.makedirs(SummaryPath)

if AppendSummary:
	fileWrite=open(SummaryPath+fileName, "a")
else:
	fileWrite=open(SummaryPath+fileName, "w")


for file in os.listdir(DataPath):
	if file.endswith(".stats"):
		fileReader = open(os.path.join(DataPath, file),"r")
		fileWrite.write(fileReader.read())
		fileReader.close()

fileWrite.close()