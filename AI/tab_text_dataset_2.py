# -*- coding: utf-8 -*-

# pip install pypiwin32
import win32gui
import time
import os
import pandas as pd

file_name = 'tab_text_dataset.csv'
browser_list = [' - Chrome', ' - Internet Explorer']

window = ''
while True:
    current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if window != current_window:
        window = current_window
        window_df = {'tab_name' : [current_window]}
        window_df = pd.DataFrame(window_df)
        print(window)

        for browser in browser_list:
            if browser in window:
                if not os.path.exists(file_name):
                    window_df.to_csv(file_name, index=False, mode='w', encoding='utf-8-sig')
                else:
                    window_df.to_csv(file_name, index=False, mode='a', encoding='utf-8-sig', header=False)
                    
    time.sleep(1)
