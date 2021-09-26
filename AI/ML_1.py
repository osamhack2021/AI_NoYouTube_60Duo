# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

file_name = 'tab_text_dataset.csv'
data = pd.read_csv(file_name, encoding=('euc-kr'), names=['tab','study'])
# 데이터 중복 제거
data.drop_duplicates(subset=['tab'], inplace=True)


X_data = data['tab']
y_data = data['study']

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_data) # X의 각 행에 토큰화를 수행
sequences = tokenizer.texts_to_sequences(X_data) # 단어를 숫자값, 인덱스로 변환하여 저장
print(sequences[:5])

word_to_index = tokenizer.word_index
vocab_size = len(word_to_index) + 1
print('단어 집합의 크기: {}'.format((vocab_size)))


X_data = sequences
print('텍스트 최대 길이 : %d' % max(len(l) for l in X_data))
print('텍스트 평균 길이 : %f' % (sum(map(len, X_data))/len(X_data)))

max_len = max(len(l) for l in X_data)
# 전체 데이터셋의 길이는 max_len으로 맞춥니다.
data = pad_sequences(X_data, maxlen = max_len)
print("훈련 데이터의 크기(shape): ", data.shape)


# 데이터셋 분류(셔플)
X_train, X_test, y_train, y_test = train_test_split(data, 
                                                    np.array(y_data), 
                                                    test_size=0.1, 
                                                    shuffle=True, 
                                                    random_state=32)

from tensorflow.keras.layers import SimpleRNN, Embedding, Dense
from tensorflow.keras.models import Sequential
model = Sequential()
model.add(Embedding(vocab_size, 32)) # 임베딩 벡터의 차원은 32
model.add(SimpleRNN(32)) # RNN 셀의 hidden_size는 32
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
history = model.fit(X_train, y_train, epochs=4, batch_size=64, validation_split=0.2)

print("\n 테스트 정확도: %.4f" % (model.evaluate(X_test, y_test)[1]*100))

epochs = range(1, len(history.history['acc']) + 1)
plt.plot(epochs, history.history['loss'])
plt.plot(epochs, history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()