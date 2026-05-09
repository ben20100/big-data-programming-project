# 📊 프로젝트명: [주제명]

## 1. 문제 정의
* **해결하고자 하는 문제:** [예: 배달 앱 이용 데이터를 분석하여 시간대별 수요 예측]
* **사용 데이터:** [예: 공공데이터 포털 배달 업종별 이용 통계]
* **데이터 수집 방법:** API 호출 및 CSV 샘플 수집

## 2. 기술 스택
* **Storage:** HDFS, S3
* **Processing:** **Apache Spark**, **Hive**
* **Ingestion:** **Kafka**, Python Requests
* **Infrastructure:** Docker

## 3. 구현 계획 (Pipeline)
1. **수집(Ingest):** Python으로 API 데이터를 호출하여 Kafka 브로커로 전송
2. **처리(Pipeline):** Spark Structured Streaming을 이용해 실시간 정제 및 분석
3. **적재(Store):** 정제된 데이터를 Hive Table에 파티셔닝하여 저장
4. **분석(Analyze):** Zeppelin 또는 Jupyter Notebook을 통한 데이터 시각화

## 4. Repository 구조
- `data/`: 데이터 출처 및 스키마 설명 (샘플 데이터 포함)
- `src/ingest/`: 데이터 수집 스크립트
- `src/pipeline/`: Spark/Hive 처리 로직
- `infra/`: Docker 환경 설정 파일
