pythonAnalyzerLocation = F:\Dropbox\Programmierung\StarCitizenGAnalyzer\analyzeVideo.py
pythonDataSummarizer = F:\Dropbox\Programmierung\StarCitizenGAnalyzer\dataSummarizer.py

DirectionTest(afterburner, key)
{
	ZoomIn()
	Send {V down}
	Sleep 100
	Send {V up}
	Sleep 50
	Send {Left down}
	Sleep 50
	Send {Up down}
	Sleep 50
	if (afterburner>0)
	{
		Send {LShift down}
		Sleep 50
	}
	Send {%key% down}
	Sleep 1000
	Send {F4 down}
	Sleep 50
	Send {F4 up}
	Sleep 50
	Send {%key% up}
	Sleep 50
	if(afterburner>0)
	{
		Send {LShift up}
		Sleep 50
	}
	Send {Up up}
	Sleep 50
	Send {Left up}
	Sleep 50
	Send {V down}
	Sleep 100
	Send {V up}
	Sleep 50
	Sleep 4000
	Send {F4 down}
	Sleep 50
	Send {F4 up}
}

ZoomIn()
{
	Send {LAlt down}
	Sleep 50
	Loop, 100
	{
		Send {WheelUp}
		Sleep 50
	}
	Send {LAlt up}
	Sleep 50
	
}

BasicAcceleration(aft)
{
	DirectionTest(aft, "w")
	Sleep 100
	DirectionTest(aft, "s")
	Sleep 100
	DirectionTest(aft, "a")
	Sleep 100
	DirectionTest(aft, "d")
	Sleep 100
	DirectionTest(aft, "Space")
	Sleep 100
	DirectionTest(aft, "LCtrl")
	Sleep 100
}

TimeToOverheatOneDirection(key)
{
	ZoomIn()
	Send {V down}
	Sleep 100
	Send {V up}
	Sleep 50
	Send {Left down}
	Sleep 50
	Send {Up down}
	Sleep 50
	Send {LShift down}
	Sleep 50
	Send {%key% down}
	Sleep 30000
	Send {F4 down}
	Sleep 50
	Send {F4 up}
	Sleep 50
	Send {%key% up}
	Sleep 50
	Send {LShift up}
	Sleep 50
	Send {Up up}
	Sleep 50
	Send {Left up}
	Sleep 50
	Send {V down}
	Sleep 100
	Send {V up}
	Sleep 10000
	Send {F4 down}
	Sleep 50
	Send {F4 up}
	Sleep 50	
}

TimeToOverheat()
{
	TimeToOverheatOneDirection("w")
	Sleep 10000
	TimeToOverheatOneDirection("s")
	Sleep 10000
	TimeToOverheatOneDirection("a")
	Sleep 10000
	TimeToOverheatOneDirection("d")
	Sleep 10000
	TimeToOverheatOneDirection("Space")
	Sleep 10000
	TimeToOverheatOneDirection("LCtrl")
	Sleep 10000
}

StartStopRecording()
{
	Sleep 100
	Send {LAlt down}
	Sleep 50
	Send {F9 down}
	Sleep 100
	Send {F9 up}
	Sleep 50
	Send {LAlt up}
	Sleep 100
}

StartPythonScript(scriptPath, Arg)
{
	commands=
		(join&
		python "%scriptPath%" "%Arg%"`n
		)
	Run, cmd /c %commands%  
}

while 2>1
{
	InputBox, Ship, SCShip, Please enter a ship brand with ship name seperated by a minus, , 420, 150
	if ErrorLevel
	{
		MSGBox, 4, , Are you finished and you want to summarize all the Video data? 
		IfMsgBox, No 
			ExitApp
		Else
			StartPythonScript(pythonDataSummarizer, Ship)
	}
	Sleep 5000
	Loop, 100
	{
		Send {WheelUp}
		Sleep 50
	}
	StartStopRecording()
	Sleep 500
	BasicAcceleration(0)
	Sleep 1000
	BasicAcceleration(1)
	Sleep 10000
	TimeToOverheat()
	Sleep 100
	StartStopRecording()
	Sleep 5000()
	StartPythonScript(pythonAnalyzerLocation, Ship)
}

