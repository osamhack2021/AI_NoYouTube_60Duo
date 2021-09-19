# pip install pypiwin32
import win32gui
import time
import csv

file_name = 'tab_text_dataset.csv'
browser_list = [' - Chrome', ' - Internet Explorer']

window = ''
while True:
    current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if window != current_window:
        window = current_window
        print(window)
        
        for browser in browser_list:
            if browser in window:
                window = window.replace(browser,'')
                with open(file_name, 'a', newline='') as f:
                    wr = csv.writer(f, lineterminator='\n')
                    wr.writerow([window])
                f.close()
                window = window + browser                
    time.sleep(1)