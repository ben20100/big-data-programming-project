from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def run_rf(df, league_name):

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

    rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_split=10,
        random_state=42
    )

    rf.fit(X_train,y_train)

    print("\n====================")
    print(league_name)
    print("====================")

    print("Accuracy =",rf.score(X_test,y_test))

    print("\nFeature Importance")

    for name,importance in zip(
        X.columns,
        rf.feature_importances_
    ):
        print(name,importance)

run_rf(epl_df,"EPL")
run_rf(bund_df,"Bundesliga")
run_rf(liga_df,"La Liga")
