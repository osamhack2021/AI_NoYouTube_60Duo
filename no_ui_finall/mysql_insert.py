import re
import win32gui
import time
import pymysql

browser_list = ['Chrome', 'Internet Explorer','Microsoft Edge']
window = ''
while True:
    current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow()) 
    if window != current_window:
        
        window = current_window
        # 한글,영어, 공백 남기고 다제거
        re_window = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣A-Za-z0-9 ]","",window)
        
        for browser in browser_list:
            if browser in window:
                re_window = re_window.replace(browser,'')
                date = time.strftime('%Y-%m-%d', time.localtime(time.time())) # 현재 날짜
                sqldata = (re_window, date)
                print(re_window)
                
                #db 연결
                conn = pymysql.connect(
                    user='monitoring', 
                    password='rnswl',          
                    host='172.28.113.191',  # 서버 주소
                    db='monitoring_data',   # db 이름
                    charset='utf8'
                )
                cursor = conn.cursor(pymysql.cursors.DictCursor) #db문 열기
                sql = "INSERT INTO crawling_data (tab, date) VALUES (%s, %s)" # crawling_data 테이블에 삽입
                cursor.execute(sql, sqldata)
                conn.commit()
                conn.close() #db문 닫기
    time.sleep(1)