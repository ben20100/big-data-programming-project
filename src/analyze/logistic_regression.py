import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# 사용할 변수
features = [
    "shoton_diff",
    "corner_diff",
    "foul_diff",
    "possession_diff",
    "home_win_rate",
    "away_win_rate",
    "win_rate_diff"
]

# X, y 생성
X = df[features]
y = df["win"]

# Train/Test 분리
X_train,X_test,y_train,y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# 모델 생성
lr = LogisticRegression(max_iter=1000)

# 학습
lr.fit(X_train,y_train)

# 정확도
print("Accuracy =",lr.score(X_test,y_test))

# 계수 출력
print("\nCoefficients")
for name,coef in zip(X.columns,lr.coef_[0]):
    print(name,coef)
