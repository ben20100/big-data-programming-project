# ============================================================
# 1. 라이브러리 import
# ============================================================

import re
from pyspark.sql.functions import udf, col, when
from pyspark.sql.types import IntegerType

# ============================================================
# 2. Match 데이터 로드
# ============================================================

match_df = spark.read \
.option("header","true") \
.option("inferSchema","true") \
.csv("/user/maria_dev/football/Match.csv")

# ============================================================
# 3. 유효슈팅 추출 함수
# ============================================================

def home_shoton(xml,home_team):
    if xml is None:
        return 0

    pattern=(
        "<stats><shoton>1</shoton></stats>.*?"
        "<team>{}</team>".format(home_team)
    )

    return len(re.findall(pattern,xml))

def away_shoton(xml,away_team):
    if xml is None:
        return 0

    pattern=(
        "<stats><shoton>1</shoton></stats>.*?"
        "<team>{}</team>".format(away_team)
    )

    return len(re.findall(pattern,xml))

# ============================================================
# 4. 코너킥 추출 함수
# ============================================================

def home_corner(xml,home_team):
    if xml is None:
        return 0

    pattern=(
        "<corners>1</corners>.*?"
        "<team>{}</team>".format(home_team)
    )

    return len(re.findall(pattern,xml))

def away_corner(xml,away_team):
    if xml is None:
        return 0

    pattern=(
        "<corners>1</corners>.*?"
        "<team>{}</team>".format(away_team)
    )

    return len(re.findall(pattern,xml))

# ============================================================
# 5. 파울 추출 함수
# ============================================================

def home_foul(xml,home_team):
    if xml is None:
        return 0

    pattern=(
        "<foulscommitted>1</foulscommitted>.*?"
        "<team>{}</team>".format(home_team)
    )

    return len(re.findall(pattern,xml))

def away_foul(xml,away_team):
    if xml is None:
        return 0

    pattern=(
        "<foulscommitted>1</foulscommitted>.*?"
        "<team>{}</team>".format(away_team)
    )

    return len(re.findall(pattern,xml))

# ============================================================
# 6. 점유율 추출 함수
# ============================================================

def home_possession(xml):
    if xml is None:
        return None

    vals=re.findall(
        "<homepos>(\d+)</homepos>",
        xml
    )

    if len(vals)==0:
        return None

    return int(vals[-1])

def away_possession(xml):
    if xml is None:
        return None

    vals=re.findall(
        "<awaypos>(\d+)</awaypos>",
        xml
    )

    if len(vals)==0:
        return None

    return int(vals[-1])

# ============================================================
# 7. UDF 생성
# ============================================================

home_shoton_udf=udf(home_shoton,IntegerType())
away_shoton_udf=udf(away_shoton,IntegerType())

home_corner_udf=udf(home_corner,IntegerType())
away_corner_udf=udf(away_corner,IntegerType())

home_foul_udf=udf(home_foul,IntegerType())
away_foul_udf=udf(away_foul,IntegerType())

home_pos_udf=udf(home_possession,IntegerType())
away_pos_udf=udf(away_possession,IntegerType())

# ============================================================
# 8. 통계 컬럼 생성
# ============================================================

analysis_df=match_df \
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

# ============================================================
# 9. 승패 라벨 및 차이값 생성
# ============================================================

analysis_df=analysis_df \
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
) \
.withColumn(
    "shoton_diff",
    col("home_shoton_count")-
    col("away_shoton_count")
) \
.withColumn(
    "corner_diff",
    col("home_corner_count")-
    col("away_corner_count")
) \
.withColumn(
    "foul_diff",
    col("home_foul_count")-
    col("away_foul_count")
) \
.withColumn(
    "possession_diff",
    col("home_possession")-
    col("away_possession")
)

# ============================================================
# 10. 리그 분리
# ============================================================

epl_df=analysis_df.filter(col("league_id")==1729)
bund_df=analysis_df.filter(col("league_id")==7809)
liga_df=analysis_df.filter(col("league_id")==21518)

# ============================================================
# 11. 상관계수 분석
# ============================================================

print("=== EPL ===")
print("ShotOn :",epl_df.stat.corr("shoton_diff","win"))
print("Corner :",epl_df.stat.corr("corner_diff","win"))
print("Foul :",epl_df.stat.corr("foul_diff","win"))
print("Possession :",epl_df.stat.corr("possession_diff","win"))

print("=== Bundesliga ===")
print("ShotOn :",bund_df.stat.corr("shoton_diff","win"))
print("Corner :",bund_df.stat.corr("corner_diff","win"))
print("Foul :",bund_df.stat.corr("foul_diff","win"))
print("Possession :",bund_df.stat.corr("possession_diff","win"))

print("=== La Liga ===")
print("ShotOn :",liga_df.stat.corr("shoton_diff","win"))
print("Corner :",liga_df.stat.corr("corner_diff","win"))
print("Foul :",liga_df.stat.corr("foul_diff","win"))
print("Possession :",liga_df.stat.corr("possession_diff","win"))
