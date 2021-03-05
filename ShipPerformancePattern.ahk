pythonAnalyzerLocation = F:\Dropbox\Programmierung\StarCitizenGAnalyzer\analyzeVideo.py
pythonDataSummarizer = F:\Dropbox\Programmierung\StarCitizenGAnalyzer\dataSummarizer.py

DirectionTest(afterburner, key, key2, key3 )
{
	ZoomIn()
	Send {V down}
	Sleep 20
	Send {V up}
	Sleep 17
	; Send {Left down}
	; Sleep 17
	; Send {Up down}
	; Sleep 17
	if (afterburner>0)
	{
		Send {LShift down}
		Sleep 17
	}
	Send {%key% down}
	Sleep 17
	if ( key2 <> "none")
	{
		Send {%key2% down}
		Sleep 17
	}
	if ( key3 <> "none")
	{
		Send {%key3% down}
		Sleep 17
	}
	Sleep 2000
	Send {F4 down}
	Sleep 17
	Send {F4 up}
	Sleep 17
	if ( key3 <> "none")
	{
		Send {%key3% up}
		Sleep 17
	}
	if ( key2 <> "none")
	{
		Send {%key2% up}
		Sleep 17
	}
	Send {%key% up}
	Sleep 17
	if(afterburner>0)
	{
		Send {LShift up}
		Sleep 17
	}
	; Send {Up up}
	; Sleep 17
	; Send {Left up}
	; Sleep 17
	Send {V down}
	Sleep 20
	Send {V up}
	Sleep 17
	Sleep 11000
	Send {F4 down}
	Sleep 17
	Send {F4 up}
}

ZoomIn()
{
	Send {LAlt down}
	Sleep 17
	Loop, 100
	{
		Send {WheelUp}
		Sleep 17
	}
	Send {LAlt up}
	Sleep 17
	
}

BasicAcceleration(aft)
{
	DirectionTest(aft, "w", "none", "none")
	Sleep 20
	DirectionTest(aft, "s", "none", "none")
	Sleep 20
	DirectionTest(aft, "a", "none", "none")
	Sleep 20
	DirectionTest(aft, "d", "none", "none")
	Sleep 20
	DirectionTest(aft, "Space", "none", "none")
	Sleep 20
	DirectionTest(aft, "LCtrl", "none", "none")
	Sleep 20
	
	DirectionTest(aft, "w", "Space", "none")
	Sleep 20
	DirectionTest(aft, "w", "LCtrl", "none")
	Sleep 20
	DirectionTest(aft, "w", "a", "none")
	Sleep 20
	DirectionTest(aft, "w", "d", "none")
	Sleep 20
	DirectionTest(aft, "w", "Space", "a")
	Sleep 20
	DirectionTest(aft, "w", "Space", "d")
	Sleep 20
	DirectionTest(aft, "w", "LCtrl", "a")
	Sleep 20
	DirectionTest(aft, "w", "LCtrl", "d")
	Sleep 20
	DirectionTest(aft, "s", "Space", "none")
	Sleep 20
	DirectionTest(aft, "s", "LCtrl", "none")
	Sleep 20
	DirectionTest(aft, "s", "a", "none")
	Sleep 20
	DirectionTest(aft, "s", "d", "none")
	Sleep 20
	DirectionTest(aft, "s", "Space", "a")
	Sleep 20
	DirectionTest(aft, "s", "Space", "d")
	Sleep 20
	DirectionTest(aft, "s", "LCtrl", "a")
	Sleep 20
	DirectionTest(aft, "s", "LCtrl", "d")
	Sleep 20
	DirectionTest(aft, "LCtrl", "a", "none")
	Sleep 20
	DirectionTest(aft, "LCtrl", "d", "none")
	Sleep 20
	DirectionTest(aft, "Space", "a", "none")
	Sleep 20
	DirectionTest(aft, "Space", "d", "none")
	Sleep 20
}

TimeToOverheatOneDirection(key, key2, key3)
{
	ZoomIn()
	Send {V down}
	Sleep 20
	Send {V up}
	Sleep 17
	; Send {Left down}
	; Sleep 17
	; Send {Up down}
	; Sleep 17
	Send {LShift down}
	Sleep 17
	Send {%key% down}
	Sleep 17
	if ( key2 <> "none")
	{
		Send {%key2% down}
		Sleep 17
	}
	if ( key3 <> "none")
	{
		Send {%key3% down}
		Sleep 17
	}
	Sleep 30000
	if ( key3 <> "none")
	{
		Send {%key3% up}
		Sleep 17
	}
	if ( key2 <> "none")
	{
		Send {%key2% up}
		Sleep 17
	}
	Send {F4 down}
	Sleep 17
	Send {F4 up}
	Sleep 17
	Send {%key% up}
	Sleep 17
	Send {LShift up}
	Sleep 17
	Send {Up up}
	Sleep 17
	Send {Left up}
	Sleep 17
	Send {V down}
	Sleep 20
	Send {V up}
	Sleep 2000
	Send {F4 down}
	Sleep 17
	Send {F4 up}
	Sleep 17	
}

TimeToOverheat()
{
	TimeToOverheatOneDirection("w", "none", "none")
	Sleep 20000
	TimeToOverheatOneDirection("s", "none", "none")
	Sleep 20000
	TimeToOverheatOneDirection("a", "none", "none")
	Sleep 20000
	TimeToOverheatOneDirection("d", "none", "none")
	Sleep 20000
	TimeToOverheatOneDirection("Space", "none", "none")
	Sleep 20000
	TimeToOverheatOneDirection("LCtrl", "none", "none")
	Sleep 20000
	
	
	TimeToOverheatOneDirection("w", "Space", "none")
	Sleep 20000
	TimeToOverheatOneDirection("w", "LCtrl", "none")
	Sleep 20000
	TimeToOverheatOneDirection("w", "a", "none")
	Sleep 20000
	TimeToOverheatOneDirection("w", "d", "none")
	Sleep 20000
	TimeToOverheatOneDirection("w", "Space", "a")
	Sleep 20000
	TimeToOverheatOneDirection("w", "Space", "d")
	Sleep 20000
	TimeToOverheatOneDirection("w", "LCtrl", "a")
	Sleep 20000
	TimeToOverheatOneDirection("w", "LCtrl", "d")
	Sleep 20000
	TimeToOverheatOneDirection("s", "Space", "none")
	Sleep 20000
	TimeToOverheatOneDirection("s", "LCtrl", "none")
	Sleep 20000
	TimeToOverheatOneDirection("s", "a", "none")
	Sleep 20000
	TimeToOverheatOneDirection("s", "d", "none")
	Sleep 20000
	TimeToOverheatOneDirection("s", "Space", "a")
	Sleep 20000
	TimeToOverheatOneDirection("s", "Space", "d")
	Sleep 20000
	TimeToOverheatOneDirection("s", "LCtrl", "a")
	Sleep 20000
	TimeToOverheatOneDirection("s", "LCtrl", "d")
	Sleep 20000
	TimeToOverheatOneDirection("LCtrl", "a", "none")
	Sleep 20000
	TimeToOverheatOneDirection("LCtrl", "d", "none")
	Sleep 20000
	TimeToOverheatOneDirection("Space", "a", "none")
	Sleep 20000
	TimeToOverheatOneDirection("Space", "d", "none")
	Sleep 20000
}

StartStopRecording()
{
	Sleep 20
	Send {LAlt down}
	Sleep 17
	Send {F9 down}
	Sleep 20
	Send {F9 up}
	Sleep 17
	Send {LAlt up}
	Sleep 20
}

StartPythonScript(scriptPath, Arg, Arg2)
{
	commands=
		(join&
		python "%scriptPath%" "%Arg%" "%Arg2%"`n
		)
	Run, cmd /c %commands%  
}
Short:= 1
while 2>1
{
	InputBox, Ship, SCShip, Please enter a ship brand with ship name seperated by a minus, , 420, 150
	if ErrorLevel
	{
		MSGBox, 4, , Are you finished and you want to summarize all the Video data? 
		IfMsgBox, No 
			ExitApp
		Else
			StartPythonScript(pythonDataSummarizer, Ship, Short)
	}
	MSGBox, 4, , Press Yes for Short Analysis, no or Cancel for extensive testing? 
		IfMsgBox, No 
			Short:=-1
		Else
			Short:=1
	Sleep 1700
	Loop, 100
	{
		Send {WheelUp}
		Sleep 17
	}
	StartStopRecording()
	Sleep 170
	BasicAcceleration(0)
	Sleep 200
	BasicAcceleration(1)
	if Short < 0
	{
		Sleep 2000
		TimeToOverheat()	
	}
	Sleep 20
	StartStopRecording()
	Sleep 1700()
	InputBox, ProcessIt, Processing, Press yes to start processing, , 420, 
	if ErrorLevel
	{
		ExitApp
	}
	StartPythonScript(pythonAnalyzerLocation, Ship, Short)
}

