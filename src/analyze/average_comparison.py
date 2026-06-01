# ============================================================
# 평균 비교 분석
# 승리팀(win=1) vs 패배팀(win=0)
# ============================================================

import re

from pyspark.sql.functions import *
from pyspark.sql.types import *

from utils.feature_extraction import *

# ============================================================
# 1. Match 데이터 로드
# ============================================================

match_df = spark.read \
.option("header","true") \
.option("inferSchema","true") \
.csv("/user/maria_dev/football/Match.csv")

# ============================================================
# 2. UDF 생성
# ============================================================

home_shoton_udf = udf(home_shoton,IntegerType())
away_shoton_udf = udf(away_shoton,IntegerType())

home_corner_udf = udf(home_corner,IntegerType())
away_corner_udf = udf(away_corner,IntegerType())

home_foul_udf = udf(home_foul,IntegerType())
away_foul_udf = udf(away_foul,IntegerType())

home_pos_udf = udf(home_possession,IntegerType())
away_pos_udf = udf(away_possession,IntegerType())

# ============================================================
# 3. 분석용 DataFrame 생성
# ============================================================

analysis_df = match_df \
.withColumn(
    "home_shoton_count",
    home_shoton_udf("shoton","home_team_api_id")
) \
.withColumn(
    "away_shoton_count",
    away_shoton_udf("shoton","away_team_api_id")
) \
.withColumn(
    "home_corner_count",
    home_corner_udf("corner","home_team_api_id")
) \
.withColumn(
    "away_corner_count",
    away_corner_udf("corner","away_team_api_id")
) \
.withColumn(
    "home_foul_count",
    home_foul_udf("foulcommit","home_team_api_id")
) \
.withColumn(
    "away_foul_count",
    away_foul_udf("foulcommit","away_team_api_id")
) \
.withColumn(
    "home_possession",
    home_pos_udf("possession")
) \
.withColumn(
    "away_possession",
    away_pos_udf("possession")
)

analysis_df = analysis_df \
.filter(
    col("home_team_goal") != col("away_team_goal")
) \
.withColumn(
    "win",
    when(
        col("home_team_goal") >
        col("away_team_goal"),
        1
    ).otherwise(0)
)

# ============================================================
# 4. 리그 분리
# ============================================================

epl_df = analysis_df.filter(col("league_id")==1729)

bund_df = analysis_df.filter(col("league_id")==7809)

liga_df = analysis_df.filter(col("league_id")==21518)

# ============================================================
# 5. 평균 비교 함수
# ============================================================

def compare_average(df,column_name,league_name):

    print("\n"+"="*50)
    print(f"{league_name} - {column_name}")
    print("="*50)

    df.groupBy("win") \
    .avg(column_name) \
    .orderBy("win") \
    .show()

# ============================================================
# 6. 유효슈팅 평균 비교
# ============================================================

compare_average(epl_df,"home_shoton_count","EPL")
compare_average(bund_df,"home_shoton_count","Bundesliga")
compare_average(liga_df,"home_shoton_count","La Liga")

# ============================================================
# 7. 점유율 평균 비교
# ============================================================

compare_average(epl_df,"home_possession","EPL")
compare_average(bund_df,"home_possession","Bundesliga")
compare_average(liga_df,"home_possession","La Liga")

# ============================================================
# 8. 코너킥 평균 비교
# ============================================================

compare_average(epl_df,"home_corner_count","EPL")
compare_average(bund_df,"home_corner_count","Bundesliga")
compare_average(liga_df,"home_corner_count","La Liga")

# ============================================================
# 9. 파울 평균 비교
# ============================================================

compare_average(epl_df,"home_foul_count","EPL")
compare_average(bund_df,"home_foul_count","Bundesliga")
compare_average(liga_df,"home_foul_count","La Liga")
