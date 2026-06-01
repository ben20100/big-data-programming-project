#승률 변수 생성
df["home_win"] = (
    df["home_team_goal"]
    >
    df["away_team_goal"]
).astype(int)

df["away_win"] = (
    df["away_team_goal"]
    >
    df["home_team_goal"]
).astype(int)

# 홈 승리
home_win_rate = (
    df.groupby("home_team_api_id")["home_win"]
    .mean()
    .reset_index()
)

home_win_rate.columns = [
    "home_team_api_id",
    "home_win_rate"
]

#원정 승리
away_win_rate = (
    df.groupby("away_team_api_id")["away_win"]
    .mean()
    .reset_index()
)

away_win_rate.columns = [
    "away_team_api_id",
    "away_win_rate"
]

#df에 변수 조인
df = df.merge(
    home_win_rate,
    on="home_team_api_id",
    how="left"
)

df = df.merge(
    away_win_rate,
    on="away_team_api_id",
    how="left"
)

# 승률 차이 변수
df["win_rate_diff"] = (
    df["home_win_rate"]
    -
    df["away_win_rate"]
)

#로지스틱 회귀

epl_df = df[df["league_id"] == 1729].copy()
bundesliga_df = df[df["league_id"] == 7809].copy()
laliga_df = df[df["league_id"] == 10257].copy()

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

def run_lr(df, league_name):

    features = [
        "shoton_diff",
        "corner_diff",
        "foul_diff",
        "possession_diff",
        "home_win_rate",
        "away_win_rate",
        "win_rate_diff"
    ]

    X = df[features]
    y = df["win"]

    X_train,X_test,y_train,y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    lr = LogisticRegression(
        max_iter=1000
    )

    lr.fit(X_train,y_train)

    print("\n======================")
    print(league_name)
    print("======================")

    print("Accuracy =",lr.score(X_test,y_test))

    print("\nCoefficients")

    for name,coef in zip(
        X.columns,
        lr.coef_[0]
    ):
        print(name,coef)

run_lr(epl_df,"EPL")
run_lr(bundesliga_df,"Bundesliga")
run_lr(laliga_df,"La Liga")
