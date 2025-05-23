# -*- coding: utf-8 -*-
"""hands-on-ML-Basic-과제(1)-여행자보험가입예측(분류)-an example of a solution

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YRrj8kjKJpbhDJWN3NsA9nDAG1pXlS7w

여행자 보험 가입 예측 분석 과제

1. 과제 개요
여러분은 여행자 보험 회사의 데이터 분석가로서, 고객의 특성을 기반으로 여행자 보험 가입 여부를 예측하는 모델을 개발해야 합니다. 이 예측 모델은 회사의 마케팅 전략 수립과 타겟 고객 선정에 중요한 정보를 제공할 것입니다.

2. 평가 방법
모델의 성능은 ROC-AUC(Receiver Operating Characteristic - Area Under Curve) 점수를 사용하여 평가됩니다.

3. 결과 제출 형식
최종 결과물은 다음과 같은 형식의 result.csv 파일로 제출해야 합니다:
ID, TravelInsurance
1, 0
2, 1
3, 0
...
여기서 TravelInsurance는 각 고객의 보험 가입 여부 예측값으로, 0(미가입) 또는 1(가입)의 값을 가집니다.

4. 제출 요구사항
- 완성된 분석 코드(Python 스크립트 또는 Jupyter Notebook)
- result.csv 예측 결과 파일

5. 평가 기준
- 코드 구현의 정확성 및 효율성
- ROC-AUC 점수 기반 예측 성능
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score

# [1] 파일 가져오기 (2개, XX_train.csv, XX_test.csv)
XY = pd.read_csv('https://raw.githubusercontent.com/TheAILab-CodingX/hands-on-ML-Basic/refs/heads/main/insurance_train.csv')
X_submission = pd.read_csv('https://raw.githubusercontent.com/TheAILab-CodingX/hands-on-ML-Basic/refs/heads/main/insurance_test.csv')
print(XY.head(2))
print(X_submission.head(2))

X = XY.drop(columns=['TravelInsurance'])
Y = XY['TravelInsurance']
#print(X.head(2))
#print(Y.head(2))
print(X.shape, Y.shape, X_submission.shape)  # (1490, 9) (1490,) (497, 9)

# [2] 데이터 탐색 (XY.info(), X_submission.info()) 결측치, 컬럼 dtype
#X.info() #Employment Type , GraduateOrNot  , FrequentFlyer, EverTravelledAbroad
obj_columns = X.select_dtypes(include=['object']).columns
#print(X.select_dtypes(include=['object']).nunique())
#print(X_submission.select_dtypes(include=['object']).nunique())
#4개의 범주형 변수에 대해서 -> LabelEncoder 사용

# [3] 데이터 전처리
# [3-1] X, X_submission -> X_all
# [3-2] X_all : 컬럼제거, 컬럼 dtype 변경(컬럼의 값을 대체), Encoding(범주형->수치형)
# [3-3] X_all : Scaling (안함, MinMaxScaler, StandardScaler, ...)
# [3-4] X_all -> X, X_submission 분리

X_all = pd.concat([X, X_submission], axis=0)
print(X_all.head(2))
# 컬럼제거 : Unnamed: 0
# Encoding : obj_columns -> LabelEncoding
X_all = X_all.drop(columns=['Unnamed: 0'])
for colname in obj_columns:
    X_all[colname] = LabelEncoder().fit_transform(X_all[colname])

#X_all.info()

X = X_all.iloc[:len(X), :]
X_submission = X_all.iloc[len(X):, :]
print(X.shape, X_submission.shape)  # (1490, 8) (497, 8)

# [4] 모델링


# 평가 (x_train, y_train), (x_test, y_test)

# [4-1] train_test_split : (X, Y) -> (x_train, x_test, y_train, y_test)
x_train, x_test, y_train, y_test= train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=42)
#print([x.shape for x in temp])  # [(1192, 8), (298, 8), (1192,), (298,)]

# [4-2] 모델객체 생성, 학습 (x_train, y_train)
# RandomForestClassifier 모델 생성 및 학습
rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf.fit(x_train, y_train)

# [4-3] 예측
y_pred = rf.predict(x_test)
y_proba = rf.predict_proba(x_test)[:, 1]  # 양성 클래스 확률

# [4-4]정확도와 ROC AUC 스코어 평가
acc = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)

print(f'정확도(Accuracy): {acc:.4f}')
print(f'ROC AUC: {auc:.4f}')

# [5] 최종모델 선택, 예측값(X_submission), 제출파일생성
result = rf.predict(X_submission)
pd.DataFrame({'pred': result}).to_csv('result.csv', index=False)

# [6] 제출한 파일 확인
temp = pd.read_csv('result.csv')
#print(temp.shape)  # (497, 1)
print(temp.tail(10))
print(Y.value_counts(normalize=True))
print(temp['pred'].value_counts(normalize=True))