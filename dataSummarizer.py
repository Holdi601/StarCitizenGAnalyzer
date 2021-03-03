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
	
headerMain="Manufacteur,Ship,Comment,DateOfTest,NormAcc_fwd ,NormAcc_aft ,NormAcc_left ,NormAcc_right ,NormAcc_up ,NormAcc_down ,NormAcc_fwdup ,NormAcc_fwddown ,NormAcc_fwdleft ,NormAcc_fwdright ,NormAcc_fwdupleft ,NormAcc_fwdupright ,NormAcc_fwddownleft ,NormAcc_fwddownright ,NormAcc_aftup ,NormAcc_aftdown ,NormAcc_aftleft ,NormAcc_aftright ,NormAcc_aftupleft ,NormAcc_aftupright ,NormAcc_aftdownleft ,NormAcc_aftdownright ,NormAcc_downleft ,NormAcc_downright ,NormAcc_upleft ,NormAcc_upright  ,BurnAcc_fwd ,BurnAcc_aft ,BurnAcc_left ,BurnAcc_right ,BurnAcc_up ,BurnAcc_down ,BurnAcc_fwdup ,BurnAcc_fwddown ,BurnAcc_fwdleft ,BurnAcc_fwdright ,BurnAcc_fwdupleft ,BurnAcc_fwdupright ,BurnAcc_fwddownleft ,BurnAcc_fwddownright ,BurnAcc_aftup ,BurnAcc_aftdown ,BurnAcc_aftleft ,BurnAcc_aftright ,BurnAcc_aftupleft ,BurnAcc_aftupright ,BurnAcc_aftdownleft ,BurnAcc_aftdownright ,BurnAcc_downleft ,BurnAcc_downright ,BurnAcc_upleft ,BurnAcc_upright  ,BurnTime_fwd ,BurnTime_aft ,BurnTime_left ,BurnTime_right ,BurnTime_up ,BurnTime_down ,BurnTime_fwdup ,BurnTime_fwddown ,BurnTime_fwdleft ,BurnTime_fwdright ,BurnTime_fwdupleft ,BurnTime_fwdupright ,BurnTime_fwddownleft ,BurnTime_fwddownright ,BurnTime_aftup ,BurnTime_aftdown ,BurnTime_aftleft ,BurnTime_aftright ,BurnTime_aftupleft ,BurnTime_aftupright ,BurnTime_aftdownleft ,BurnTime_aftdownright ,BurnTime_downleft ,BurnTime_downright ,BurnTime_upleft ,BurnTime_upright  ,CoolTime_fwd ,CoolTime_aft ,CoolTime_left ,CoolTime_right ,CoolTime_up ,CoolTime_down ,CoolTime_fwdup ,CoolTime_fwddown ,CoolTime_fwdleft ,CoolTime_fwdright ,CoolTime_fwdupleft ,CoolTime_fwdupright ,CoolTime_fwddownleft ,CoolTime_fwddownright ,CoolTime_aftup ,CoolTime_aftdown ,CoolTime_aftleft ,CoolTime_aftright ,CoolTime_aftupleft ,CoolTime_aftupright ,CoolTime_aftdownleft ,CoolTime_aftdownright ,CoolTime_downleft ,CoolTime_downright ,CoolTime_upleft ,CoolTime_upright  ,HeatedBurnTime_fwd ,HeatedBurnTime_aft ,HeatedBurnTime_left ,HeatedBurnTime_right ,HeatedBurnTime_up ,HeatedBurnTime_down ,HeatedBurnTime_fwdup ,HeatedBurnTime_fwddown ,HeatedBurnTime_fwdleft ,HeatedBurnTime_fwdright ,HeatedBurnTime_fwdupleft ,HeatedBurnTime_fwdupright ,HeatedBurnTime_fwddownleft ,HeatedBurnTime_fwddownright ,HeatedBurnTime_aftup ,HeatedBurnTime_aftdown ,HeatedBurnTime_aftleft ,HeatedBurnTime_aftright ,HeatedBurnTime_aftupleft ,HeatedBurnTime_aftupright ,HeatedBurnTime_aftdownleft ,HeatedBurnTime_aftdownright ,HeatedBurnTime_downleft ,HeatedBurnTime_downright ,HeatedBurnTime_upleft ,HeatedBurnTime_upright\n"
headerTG = "Manufacteur,Ship,Comment,DateOfTest,type,thruster_dir_1,thruster_dir_2,thruster_dir_3,frame,Acc\n"

fileWrite.write(headerMain)
for file in os.listdir(DataPath):
	if file.endswith("_overview.stats"):
		fileReader = open(os.path.join(DataPath, file),"r")
		fileWrite.write(fileReader.read())
		fileReader.close()
fileWrite.close()

tlWrite.write(headerTG)
for file in os.listdir(DataPath):
	if file.endswith("_timeLine.stats"):
		fileReader = open(os.path.join(DataPath, file),"r")
		tlWrite.write(fileReader.read())
		fileReader.close()
tlWrite.close()