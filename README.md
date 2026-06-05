# ⚽ 유럽 축구 경기 데이터 기반 승리 요인 분석

## 📌 프로젝트 개요

본 프로젝트는 유럽 3대 축구 리그(EPL, 분데스리가, 라리가)의 경기 데이터를 활용하여 승리에 영향을 미치는 주요 요인을 분석한 빅데이터 프로젝트입니다.

축구 경기에서는 점유율, 유효슈팅, 코너킥, 파울 등 다양한 경기 지표가 발생합니다. 본 연구에서는 이러한 경기 데이터를 기반으로 승리와 가장 관련성이 높은 변수를 탐색하고, 리그별 경기 스타일 차이를 분석하였습니다.

또한 HDFS, Hive, Spark 기반의 빅데이터 처리 환경을 구축하고 머신러닝 모델을 활용하여 경기 결과 예측을 수행하였습니다.

---

# 🎯 연구 목표

1. 점유율이 실제로 승리에 영향을 미치는가?
2. 승리와 가장 관련성이 높은 변수는 무엇인가?
3. 리그마다 승리 요인이 다른가?
4. 머신러닝 모델을 통해 승패를 예측할 수 있는가?

---

# 🗂 데이터 소개

## 데이터 출처

- European Soccer Database (Kaggle)
(URL: https://www.kaggle.com/datasets/hugomathien/soccer?resource=download)

## 데이터 규모

- 약 25,000 경기 데이터
- 11개 유럽 리그
- 10,000명 이상의 선수 정보
- 원본 데이터 크기 약 300MB

## 사용 데이터

- Match
- League
- Team
- Team_Attributes
- Player_Attributes

---

# 🛠 기술 스택

| 분야 | 사용 기술 |
|--------|----------|
| 데이터 저장 | HDFS |
| 데이터 웨어하우스 | Hive |
| 데이터 분석 | Spark SQL, PySpark |
| 머신러닝 | Scikit-learn |
| 시각화 | Plotly, Matplotlib |
| 개발 언어 | Python |

---

# 📊 데이터 처리 파이프라인

```text
SQLite DB
    ↓
CSV 변환
    ↓
Google Drive 업로드
    ↓
gdown 다운로드
    ↓
HDFS 적재
    ↓
Hive 테이블 생성
    ↓
Spark SQL 분석
    ↓
PySpark 분석
    ↓
EDA
    ↓
Machine Learning
```

---

# 🔧 데이터 전처리

원본 데이터는 SQLite 형식으로 제공되었으며 CSV 형태로 변환 후 HDFS에 적재하였습니다.

경기 이벤트 데이터는 XML 형태로 저장되어 있어 PySpark UDF와 정규표현식을 활용하여 분석 가능한 형태로 변환하였습니다.

## 추출 변수

- home_shoton_count
- away_shoton_count
- home_corner_count
- away_corner_count
- home_foul_count
- away_foul_count
- home_possession
- away_possession

## 생성 변수

- shoton_diff
- corner_diff
- foul_diff
- possession_diff

추가 머신러닝 실험에서는 다음 변수를 생성하였습니다.

- home_win_rate
- away_win_rate
- win_rate_diff

무승부 경기는 제외하여 승패가 결정된 경기만 분석에 사용하였습니다.

---

# 📈 EDA 분석

## 분석 내용

- 점유율 50% 이상/미만 승률 비교
- 점유율 구간별 승률 분석
- 홈 어드밴티지 분석
- 홈팀 점유율 우세 시 승률 분석
- 승리와 경기 변수 간 상관관계 분석
- 리그별 평균 비교 분석

---

## 점유율과 승률

| 리그 | 점유율 50% 이상 승률 | 점유율 50% 미만 승률 |
|--------|--------|--------|
| EPL | 51.90% | 36.54% |
| Bundesliga | 51.72% | 36.41% |
| La Liga | 58.60% | 31.69% |

### 주요 결과

- 세 리그 모두 점유율이 높은 팀의 승률이 더 높게 나타남
- 라리가는 약 26.9%p 차이로 가장 큰 영향력을 보임
- 점유율과 승률의 관계는 라리가에서 가장 강하게 나타남

---

## 승리와의 상관관계

### 전체 리그 기준

| 변수 | 상관계수 |
|--------|--------|
| 점유율 차이 | 0.178 |
| 유효슈팅 차이 | 0.112 |
| 코너킥 차이 | 0.041 |
| 파울 차이 | -0.076 |

### 주요 결과

- 점유율 차이가 승리와 가장 높은 상관관계를 보임
- 유효슈팅은 양의 상관관계를 가짐
- 코너킥은 승리와 거의 관련이 없음
- 파울은 음의 상관관계를 보임

---

## 리그별 특징

### EPL

- 점유율 중심 리그
- 점유율 상관계수: 0.225
- 유효슈팅보다 점유율이 더 중요

### Bundesliga

- 공격 효율 중심 리그
- 유효슈팅 상관계수: 0.123
- 점유율 상관계수: 0.060

### La Liga

- 경기 지배형 리그
- 점유율 상관계수: 0.244
- 유효슈팅 상관계수: 0.189

---

# 🤖 머신러닝

## 사용 모델

- Logistic Regression
- Random Forest

## 입력 변수

- shoton_diff
- corner_diff
- foul_diff
- possession_diff

---

## 기본 모델 성능

| 리그 | Logistic Regression | Random Forest |
|--------|--------|--------|
| EPL | 63.2% | 63.0% |
| Bundesliga | 59.0% | 64.5% |
| La Liga | 64.2% | 61.8% |

---

## 승률 관련 변수 추가

### 추가 변수

- home_win_rate
- away_win_rate
- win_rate_diff

### 성능 향상 결과

| 리그 | 기존 정확도 | 향상 후 정확도 |
|--------|--------|--------|
| EPL | 63.2% | 74.0% |
| Bundesliga | 59.0% | 69.8% |
| La Liga | 64.2% | 77.9% |

### 주요 결과

- 모든 리그에서 정확도 상승
- win_rate_diff가 가장 중요한 변수로 나타남
- 팀 전력이 경기 결과를 가장 잘 설명함

---

# 🔍 핵심 인사이트

## 1. 점유율은 승리에 긍정적인 영향을 준다.

세 리그 모두 점유율이 높은 팀의 승률이 더 높게 나타났다.

## 2. 리그별 승리 공식이 다르다.

- EPL → 점유율 중심 리그
- Bundesliga → 공격 효율 중심 리그
- La Liga → 점유율 + 공격 효율 중심 리그

## 3. 점유율은 가장 강력한 경기 변수였다.

상관관계 분석과 머신러닝 분석 모두에서 중요한 변수로 나타났다.

## 4. 팀 전력이 경기 결과를 가장 잘 설명한다.

승률 차이(win_rate_diff)를 추가하자 최대 77.9%의 정확도를 기록하였다.

## 5. EDA와 머신러닝 결과가 동일하게 나타났다.

EDA에서 발견한 패턴이 머신러닝 모델에서도 재현되어 분석 결과의 신뢰성을 높였다.

---

# 🚀 확장 가능성

- xG(Expected Goals) 데이터 추가
- 선수 시장 가치 데이터 활용
- 실시간 경기 예측 시스템 구축
- XGBoost, LightGBM 모델 적용
- 챔피언스리그 및 타 리그 확장 분석

---

# 📁 프로젝트 구조

```text
football-bigdata-project/
│
├── README.md
├── data/
├── src/
│   ├── ingest/
│   ├── hive/
│   ├── spark/
│   └── visualization/
│
├── results/
└── report/
```

---

# 👨‍💻 개발자

전형빈

Big Data Programming Project

---

# 📚 참고자료

- European Soccer Database (Kaggle)
- Apache Hadoop
- Apache Hive
- Apache Spark
- Scikit-learn

---

# 🤖 AI 활용 내역

본 프로젝트에서는 ChatGPT를 활용하여 다음 작업을 수행하였습니다.

- XML 파싱 방법 학습
- 코드 오류 해결
- 데이터 시각화 아이디어 도출
- 보고서 작성 보조
- 그래프 표현 방식 개선
