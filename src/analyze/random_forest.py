import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

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
rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_split=10,
    random_state=42
)

# 학습
rf.fit(X_train,y_train)

# 정확도
print("Accuracy =",rf.score(X_test,y_test))

# 변수 중요도
print("\nFeature Importance")
for name,importance in zip(
    X.columns,
    rf.feature_importances_
):
    print(name,importance)
