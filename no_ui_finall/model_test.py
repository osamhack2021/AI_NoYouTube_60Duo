import win32gui
import time
from sentiment_predict import sentiment_predict
import re

browser_list = ['Chrome', 'Internet Explorer','Microsoft Edge']
window = ''
while True:
    current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if window != current_window:
        window = current_window
        for browser in browser_list:
            if browser in window:
                print(sentiment_predict(window), re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣A-Za-z0-9 ]","",window))
                
    time.sleep(1)