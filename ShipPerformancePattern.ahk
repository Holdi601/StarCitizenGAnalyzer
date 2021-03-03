pythonAnalyzerLocation = F:\Dropbox\Programmierung\StarCitizenGAnalyzer\analyzeVideo.py
pythonDataSummarizer = F:\Dropbox\Programmierung\StarCitizenGAnalyzer\dataSummarizer.py

DirectionTest(afterburner, key, key2, key3 )
{
	ZoomIn()
	Send {V down}
	Sleep 100
	Send {V up}
	Sleep 50
	; Send {Left down}
	; Sleep 50
	; Send {Up down}
	; Sleep 50
	if (afterburner>0)
	{
		Send {LShift down}
		Sleep 50
	}
	Send {%key% down}
	Sleep 50
	if ( key2 <> "none")
	{
		Send {%key2% down}
		Sleep 50
	}
	if ( key3 <> "none")
	{
		Send {%key3% down}
		Sleep 50
	}
	Sleep 1000
	Send {F4 down}
	Sleep 50
	Send {F4 up}
	Sleep 50
	if ( key3 <> "none")
	{
		Send {%key3% up}
		Sleep 50
	}
	if ( key2 <> "none")
	{
		Send {%key2% up}
		Sleep 50
	}
	Send {%key% up}
	Sleep 50
	if(afterburner>0)
	{
		Send {LShift up}
		Sleep 50
	}
	; Send {Up up}
	; Sleep 50
	; Send {Left up}
	; Sleep 50
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
	DirectionTest(aft, "w", "none", "none")
	Sleep 100
	DirectionTest(aft, "s", "none", "none")
	Sleep 100
	DirectionTest(aft, "a", "none", "none")
	Sleep 100
	DirectionTest(aft, "d", "none", "none")
	Sleep 100
	DirectionTest(aft, "Space", "none", "none")
	Sleep 100
	DirectionTest(aft, "LCtrl", "none", "none")
	Sleep 100
	
	DirectionTest(aft, "w", "Space", "none")
	Sleep 100
	DirectionTest(aft, "w", "LCtrl", "none")
	Sleep 100
	DirectionTest(aft, "w", "a", "none")
	Sleep 100
	DirectionTest(aft, "w", "d", "none")
	Sleep 100
	DirectionTest(aft, "w", "Space", "a")
	Sleep 100
	DirectionTest(aft, "w", "Space", "d")
	Sleep 100
	DirectionTest(aft, "w", "LCtrl", "a")
	Sleep 100
	DirectionTest(aft, "w", "LCtrl", "d")
	Sleep 100
	DirectionTest(aft, "s", "Space", "none")
	Sleep 100
	DirectionTest(aft, "s", "LCtrl", "none")
	Sleep 100
	DirectionTest(aft, "s", "a", "none")
	Sleep 100
	DirectionTest(aft, "s", "d", "none")
	Sleep 100
	DirectionTest(aft, "s", "Space", "a")
	Sleep 100
	DirectionTest(aft, "s", "Space", "d")
	Sleep 100
	DirectionTest(aft, "s", "LCtrl", "a")
	Sleep 100
	DirectionTest(aft, "s", "LCtrl", "d")
	Sleep 100
	DirectionTest(aft, "LCtrl", "a", "none")
	Sleep 100
	DirectionTest(aft, "LCtrl", "d", "none")
	Sleep 100
	DirectionTest(aft, "Space", "a", "none")
	Sleep 100
	DirectionTest(aft, "Space", "d", "none")
	Sleep 100
}

TimeToOverheatOneDirection(key, key2, key3)
{
	ZoomIn()
	Send {V down}
	Sleep 100
	Send {V up}
	Sleep 50
	; Send {Left down}
	; Sleep 50
	; Send {Up down}
	; Sleep 50
	Send {LShift down}
	Sleep 50
	Send {%key% down}
	Sleep 50
	if ( key2 <> "none")
	{
		Send {%key2% down}
		Sleep 50
	}
	if ( key3 <> "none")
	{
		Send {%key3% down}
		Sleep 50
	}
	Sleep 30000
	if ( key3 <> "none")
	{
		Send {%key3% up}
		Sleep 50
	}
	if ( key2 <> "none")
	{
		Send {%key2% up}
		Sleep 50
	}
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
			StartPythonScript(pythonDataSummarizer, Ship)
	}
	MSGBox, 4, , Press Yes for Short Analysis, no or Cancel for extensive testing? 
		IfMsgBox, No 
			Short:=-1
		Else
			Short:=1
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
	if Short < 0
	{
		Sleep 10000
		TimeToOverheat()
		Sleep 100
		StartStopRecording()
		Sleep 5000()
	}
	InputBox, ProcessIt, Processing, Press yes to start processing, , 420, 
	if ErrorLevel
	{
		ExitApp
	}
	StartPythonScript(pythonAnalyzerLocation, Ship, Short)
}

