# 리그 정확도 시각화
import pandas as pd
import plotly.express as px

acc_df = pd.DataFrame({
    "League": ["EPL","EPL","Bundesliga","Bundesliga","La Liga","La Liga"],
    "Model": ["Logistic Regression","Random Forest"]*3,
    "Accuracy": [73.84,72.73,69.82,69.82,77.95,75.20]
})

fig = px.bar(
    acc_df,
    x="League",
    y="Accuracy",
    color="Model",
    barmode="group",
    text="Accuracy",
    title="Model Accuracy by League"
)

fig.update_traces(texttemplate='%{text:.1f}%')
fig.update_layout(yaxis_title="Accuracy (%)")

fig.show()

#로지스틱 회귀 계수 히트맵
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

coef_df=pd.DataFrame({
    "shoton_diff":[-0.057,-0.004,0.031],
    "corner_diff":[-0.067,-0.013,-0.049],
    "foul_diff":[-0.012,-0.045,-0.006],
    "possession_diff":[0.004,-0.025,-0.020],
    "home_win_rate":[1.625,1.897,1.811],
    "away_win_rate":[-1.620,-1.631,-1.661],
    "win_rate_diff":[3.728,3.527,3.472]
},index=["EPL","Bundesliga","La Liga"])

plt.figure(figsize=(10,5))

sns.heatmap(
    coef_df,
    annot=True,
    cmap="RdBu_r",
    center=0,
    fmt=".2f"
)

plt.title("Logistic Regression Coefficients by League")
plt.tight_layout()
plt.show()

#랜덤 포레스트 중요도 (3개 리그 평균)
import pandas as pd
import plotly.express as px

rf_df=pd.DataFrame({
    "Feature":[
        "ShotOn",
        "Corner",
        "Foul",
        "Possession",
        "Home Win Rate",
        "Away Win Rate",
        "Win Rate Diff"
    ],
    "Importance":[
        (0.076+0.073+0.074)/3,
        (0.105+0.096+0.080)/3,
        (0.087+0.102+0.078)/3,
        (0.117+0.141+0.128)/3,
        (0.146+0.162+0.148)/3,
        (0.148+0.120+0.156)/3,
        (0.320+0.307+0.336)/3
    ]
})

rf_df=rf_df.sort_values(
    by="Importance",
    ascending=True
)

fig=px.bar(
    rf_df,
    x="Importance",
    y="Feature",
    orientation="h",
    text="Importance",
    title="Average Random Forest Feature Importance"
)

fig.update_traces(
    texttemplate="%{text:.3f}",
    textposition="outside"
)
fig.update_layout(
    xaxis_range=[0,0.38]
)

fig.show()

#Home vs Away Win Rate 영향력 비교
import pandas as pd
import plotly.graph_objects as go

rate_df=pd.DataFrame({
    "League":["EPL","Bundesliga","La Liga"],
    "Home":[1.625,1.897,1.811],
    "Away":[1.620,1.631,1.661]
})

fig=go.Figure()

for _,row in rate_df.iterrows():

    fig.add_trace(
        go.Scatter(
            x=[row["League"],row["League"]],
            y=[row["Away"],row["Home"]],
            mode="lines",
            showlegend=False
        )
    )

fig.add_trace(
    go.Scatter(
        x=rate_df["League"],
        y=rate_df["Home"],
        mode="markers+text",
        name="Home Win Rate",
        text=rate_df["Home"].round(3),
        textposition="top center"
    )
)

fig.add_trace(
    go.Scatter(
        x=rate_df["League"],
        y=rate_df["Away"],
        mode="markers+text",
        name="Away Win Rate",
        text=rate_df["Away"].round(3),
        textposition="bottom center"
    )
)

fig.update_layout(
    title="Home vs Away Win Rate Impact",
    yaxis_title="Coefficient"
)

fig.show()

#Win Rate Diff 비교
import pandas as pd
import plotly.express as px

diff_df = pd.DataFrame({
    "League":["EPL","Bundesliga","La Liga"],
    "Coefficient":[3.728,3.527,3.472]
})

fig = px.bar(
    diff_df,
    x="League",
    y="Coefficient",
    text="Coefficient",
    title="Win Rate Difference Coefficient by League"
)

fig.update_yaxes(
    range=[3,3.8]
)

fig.update_traces(texttemplate='%{text:.3f}')

fig.show()
