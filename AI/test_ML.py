# pip install pypiwin32

import re
import win32gui
import time
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer

okt = Okt()
tokenizer = Tokenizer()
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로',
             '자','에','와','한','하다','YouTube', '검색', '네이버', 'Google',
             'Yahoo']
max_len = 20


# 2. 모델 불러오기
model = load_model('best_model.h5')

def sentiment_predict(new_sentence):
  new_sentence = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣A-Za-z0-9 ]","",new_sentence) # 한글,영어, 공백 남기고 다제거
  new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
  new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
  encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
  pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
  score = float(model.predict(pad_new)) # 예측
  if(score > 0.5):
    return "{:.2f}% 확률로 공부중 입니다.\n".format(score * 100)
  else:
    return "{:.2f}% 확률로 딴짓중 입니다.\n".format((1 - score) * 100)ㄴ

browser_list = ['Chrome', 'Internet Explorer','Microsoft Edge']
window = ''
while True:
    current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if window != current_window:
        window = current_window
        for browser in browser_list:
            if browser in window:
                print(sentiment_predict(window)
                
    time.sleep(1)