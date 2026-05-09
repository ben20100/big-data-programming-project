# 🎮 LoL 빅데이터 분석 및 실시간 승률 예측 파이프라인

## 1. 문제 정의 (Problem Definition)
본 프로젝트는 리그 오브 레전드(LoL)의 매치 데이터를 활용하여 승패에 영향을 미치는 핵심 요소들을 분석하고, 실시간 지표를 통해 승률을 예측하는 시스템을 구축하는 것을 목적으로 합니다.

### 분석 목표
* **진형별 밸런스 분석:** 블루 진형과 레드 진형의 승률 차이를 분석하여 맵 밸런스가 승패에 미치는 영향 파악.
* **조합 및 메타 분석:** 챔피언 간의 시너지(조합 승률)를 계산하고, 현재 패치 버전에서의 필승 메타 도출.
* **인게임 승률 예측:** 경기 초반(15분)까지의 골드 차이, 오브젝트 획득 등 실시간 지표를 기반으로 최종 승리 팀 예측.

### 사용 데이터
* **출처:** Riot API (Match-V5, Match Timeline 데이터)
* **특징:** 유저별 스탯, 챔피언 조합, 분 단위 골드/경험치/위치 데이터 (JSON 형식)

---

## 2. 기술 스택 (Tech Stack)
대용량 데이터의 안정적인 수집과 분산 처리를 위해 아래 도구들을 활용합니다.

* **Ingestion:** Python (Riot API Wrapper), Apache Kafka
* **Storage:** Hadoop HDFS (Raw Data), Apache Hive (Data Warehouse)
* **Processing:** Apache Spark (Batch Processing), Spark Structured Streaming (Real-time)
* **Infrastructure:** Docker (Containerization)

---

## 3. 구현 계획 (Implementation Plan)

### 단계 1: 데이터 수집 (Ingestion)
* Python 스크립트를 통해 Riot API에서 최근 매치 데이터를 호출합니다.
* 수집된 데이터를 **Apache Kafka**의 토픽(Topic)으로 전송하여 데이터 유실을 방지하고 버퍼링 역할을 수행합니다.

### 단계 2: 데이터 처리 및 저장 (ETL & Storage)
* **Apache Spark**를 사용하여 Kafka로부터 데이터를 컨슈밍하고, 복잡한 JSON 구조를 분석에 용이한 정형 데이터로 정제합니다.
* 정제된 데이터는 **HDFS**에 Parquet 형식으로 저장하며, **Apache Hive**를 통해 진형별/챔피언별로 파티셔닝된 테이블을 구축합니다.

### 단계 3: 지표 분석 및 모델링 (Analyze)
* **진형/조합 분석:** Hive 쿼리를 통해 진형별 승률 및 챔피언 시너지 점수를 산출합니다.
* **실시간 예측:** 경기 타임라인 데이터를 활용하여 특정 시점의 우세 정도를 수치화하고 승률 예측 지표를 생성합니다.

---

## 4. Repository 구조
* `data/`: 데이터 출처 및 스키마 정보 (샘플 데이터 포함)
* `src/ingest/`: Riot API 수집용 Python 스크립트
* `src/pipeline/`: Spark 정제 및 Hive 적재 로직
* `infra/`: Docker Compose 설정 파일
