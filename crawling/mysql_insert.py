# pip install pypiwin32
# pip install pymysql

import re
import win32gui
import time
import pymysql
import time

# 이모티콘제거
def deEmojify(inputString):
    return inputString.encode('euc-kr', 'ignore').decode('euc-kr')
only_BMP_pattern = re.compile("["
        u"\U00010000-\U0010FFFF"  #BMP characters 이외
                           "]+", flags=re.UNICODE)

file_name = 'tab_text_dataset.csv'
browser_list = [' - Chrome', ' - Internet Explorer',' - Microsoft Edge']

window = ''
while True:
    current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if window != current_window:
        window = current_window
        no_emoji = deEmojify(window)
        no_emoji = only_BMP_pattern.sub(r'', no_emoji)
        
        for browser in browser_list:
            if browser in window:
                no_emoji = no_emoji.replace(browser,'')
                date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                sqldata = (no_emoji, date)
                #db 연결
                conn = pymysql.connect(
                    user='monitoring', 
                    password='rnswl', 
                    host='서버컴퓨터주소', 
                    db='monitoring_data', 
                    charset='utf8'
                )
                cursor = conn.cursor(pymysql.cursors.DictCursor) #db문 열기
                sql = "INSERT INTO crawling_data (tab, date) VALUES (%s, %s)"
                cursor.execute(sql, sqldata)
                conn.commit()
                conn.close() #db문 닫기
    time.sleep(1)