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
}

ZoomIn()