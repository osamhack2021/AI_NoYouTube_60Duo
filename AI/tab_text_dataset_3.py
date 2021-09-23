# pip install pypiwin32

# 이모티콘제거
def deEmojify(inputString):
    return inputString.encode('euc-kr', 'ignore').decode('euc-kr')

import re
only_BMP_pattern = re.compile("["
        u"\U00010000-\U0010FFFF"  #BMP characters 이외
                           "]+", flags=re.UNICODE)

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
        no_emoji = deEmojify(window)
        no_emoji = only_BMP_pattern.sub(r'', no_emoji)
        print(no_emoji)
        
        for browser in browser_list:
            if browser in window:
                no_emoji = no_emoji.replace(browser,'')
                with open(file_name, 'a', newline='') as f:
                    wr = csv.writer(f)
                    wr.writerow([no_emoji])
                f.close()
    time.sleep(1)