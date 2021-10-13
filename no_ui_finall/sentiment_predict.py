# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re
from tqdm import tqdm
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

file_name = 'tab_text_dataset.csv'
data = pd.read_csv(file_name, encoding=('cp949'), names=['tab','study'])
data.drop_duplicates(subset=['tab'], inplace=True) # 데이터 중복 제거

# 영어,한글, 공백 남기고 제거
X_data = np.array(data['tab'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣A-Za-z0-9 ]",""))
y_data = np.array(data['study'])

#불용어 목록
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로',
             '자','에','와','한','하다','YouTube', '검색', '네이버', 'Google',
             'Yahoo']

okt = Okt()
X_train = []
for sentence in tqdm(X_data):
    tokenized_sentence = okt.morphs(sentence, stem=True) # 토큰화
    stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거
    X_train.append(stopwords_removed_sentence)
    
# 정수인코딩
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)

# 빈도수 낮은 단어 검색
threshold = 3
total_cnt = len(tokenizer.word_index) # 단어의 수
rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

# 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
for key, value in tokenizer.word_counts.items():
    total_freq = total_freq + value

    # 단어의 등장 빈도수가 threshold보다 작으면
    if(value < threshold):
        rare_cnt = rare_cnt + 1
        rare_freq = rare_freq + value

# 0번 패딩 토큰을 고려하여 + 1
vocab_size = total_cnt - rare_cnt + 1

# 단어 정수화
tokenizer = Tokenizer(vocab_size) 
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)


max_len = 20

loaded_model = load_model('best_model.h5')

def sentiment_predict(new_sentence):
    new_sentence = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣A-Za-z0-9 ]","",new_sentence) # 한글,영어, 공백 남기고 다제거
    new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    score = float(loaded_model.predict(pad_new)) # 예측
    if(score > 0.5):
      return "{:.2f}% 확률로 공부중입니다.\n".format(score * 100)
    else:
      return "{:.2f}% 확률로 딴짓중 입니다..\n".format((1 - score) * 100)
    