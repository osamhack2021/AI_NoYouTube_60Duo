# 현재창 정보 가져오기
import win32gui
import time

window = ''
while True:
    current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if window != current_window:
        window = current_window
        print(window)
    time.sleep(1)
    
    