import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# 점유율 50% 이상 50% 미만 승률 비교 그래프

import pandas as pd
import plotly.graph_objects as go

df = pd.DataFrame({
    'League': ['EPL', 'Bundesliga', 'La Liga'],
    'Above50': [51.90, 51.72, 58.60],
    'Below50': [36.54, 36.41, 31.69]
})

df['Gap'] = df['Above50'] - df['Below50']

fig = go.Figure()

# 점유율 50% 이상
fig.add_trace(
    go.Bar(
        x=df['League'],
        y=df['Above50'],
        name='Possession ≥ 50%',
        marker_color='royalblue',
        text=[f'{v:.2f}%' for v in df['Above50']],
        textposition='outside'
    )
)

# 점유율 50% 미만
fig.add_trace(
    go.Bar(
        x=df['League'],
        y=df['Below50'],
        name='Possession < 50%',
        marker_color='crimson',
        text=[f'{v:.2f}%' for v in df['Below50']],
        textposition='outside'
    )
)

# 차이 표시용 선
for i, row in df.iterrows():

    fig.add_shape(
        type="line",
        x0=row['League'],
        x1=row['League'],
        y0=row['Below50'],
        y1=row['Above50'],
        line=dict(
            color="black",
            width=3,
            dash="dot"
        )
    )

    # 라리가만 강조
    if row['League'] == 'La Liga':
        bgcolor = 'yellow'
        bordercolor = 'orange'
        font_size = 14
    else:
        bgcolor = 'white'
        bordercolor = 'black'
        font_size = 12

    fig.add_annotation(
        x=row['League'],
        y=(row['Above50'] + row['Below50']) / 2,
        text=f"+{row['Gap']:.2f}%p",
        showarrow=False,
        bgcolor=bgcolor,
        bordercolor=bordercolor,
        borderwidth=1,
        font=dict(
            size=font_size,
            color='black'
        )
    )

fig.update_layout(
    title='점유율 50%이상 승률 VS 50%미만 승률',
    xaxis_title='리그',
    yaxis_title='승률 (%)',
    barmode='group',
    template='plotly_white',
    height=600,
    width=900,
    font=dict(size=14)
)

fig.show()

# ============================================================
# 점유율 구간별 승률 그래프

import pandas as pd
import plotly.express as px

# 데이터
df = pd.DataFrame({
    "Possession": [
        "Under 40%", "40-50%", "50-60%", "Over 60%",
        "Under 40%", "40-50%", "50-60%", "Over 60%",
        "Under 40%", "40-50%", "50-60%", "Over 60%"
    ],
    "WinRate": [
        29.64, 39.78, 46.28, 59.11,   # EPL
        31.65, 38.73, 48.68, 46.64,   # Bundesliga
        19.38, 38.65, 51.20, 53.93    # La Liga
    ],
    "League": [
        "EPL", "EPL", "EPL", "EPL",
        "Bundesliga", "Bundesliga", "Bundesliga", "Bundesliga",
        "La Liga", "La Liga", "La Liga", "La Liga"
    ]
})

# 순서 지정
category_order = [
    "Under 40%",
    "40-50%",
    "50-60%",
    "Over 60%"
]

fig = px.line(
    df,
    x="Possession",
    y="WinRate",
    color="League",
    markers=True,
    category_orders={"Possession": category_order},
    title="점유율 구간별 승률"
)

fig.update_traces(
    line=dict(width=4),
    marker=dict(size=10)
)

fig.update_layout(
    template="plotly_white",
    height=600,
    width=900,
    xaxis_title="점유율 구간",
    yaxis_title="승률 (%)",
    font=dict(size=14),
    legend_title="리그"
)

# 데이터 값 표시
fig.update_traces(
    text=df["WinRate"],
    textposition="top center"
)

fig.show()

# ============================================================

#리그별 특성(유효슛, 코너킥, 파울 수, 점유율)과 승리와의 상관관계
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

corr_df = pd.DataFrame(
    [
        [0.088, 0.059, -0.070, 0.225],
        [0.124, 0.047, -0.045, 0.060],
        [0.189, 0.072, -0.040, 0.244]
    ],
    index=["EPL","Bundesliga","La Liga"],
    columns=[
        "ShotOn",
        "Corner",
        "Foul",
        "Possession"
    ]
)

plt.figure(figsize=(8,5))

sns.heatmap(
    corr_df,
    annot=True,
    fmt=".3f",
    cmap="coolwarm",
    center=0,
    square=True,
    linewidths=1,
    cbar_kws={
        "label":"상관계수"
    }
)

plt.title(
    "경기 변수와 승리와의 상관계수",
    fontsize=14,
    pad=15
)

plt.xlabel("경기 변수")
plt.ylabel("리그")

plt.tight_layout()
plt.show()

# ============================================================

#승리팀 패배팀 유효슈팅 개수 차이

import pandas as pd
import plotly.graph_objects as go

shot_df = pd.DataFrame({
    "League":["EPL","Bundesliga","La Liga"],
    "Win":[5.08,5.27,5.38],
    "Loss":[4.92,4.71,4.76]
})

line_colors = [
    "royalblue",
    "mediumpurple",
    "hotpink"
]

fig = go.Figure()

for i,row in shot_df.iterrows():

    fig.add_trace(
        go.Scatter(
            x=[row["League"],row["League"]],
            y=[row["Loss"],row["Win"]],
            mode="lines",
            line=dict(
                color=line_colors[i],
                width=4
            ),
            showlegend=False
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[row["League"]],
            y=[row["Loss"]],
            mode="markers+text",
            name="패배팀",
            showlegend=(i==0),
            text=[f'{row["Loss"]:.2f}'],
            textposition="bottom center",
            marker=dict(
                size=12,
                color="red"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[row["League"]],
            y=[row["Win"]],
            mode="markers+text",
            name="승리팀",
            showlegend=(i==0),
            text=[f'{row["Win"]:.2f}'],
            textposition="top center",
            marker=dict(
                size=12,
                color="blue"
            )
        )
    )

fig.update_layout(
    title="승리팀 VS 패배팀 유효슈팅 개수",
    title_x=0.5,
    width=900,
    height=600,
    yaxis_title="유효슈팅 개수",
    xaxis_title="리그",
    yaxis=dict(range=[4.5,5.6])
)

fig.show()

# ============================================================

#승리팀 패배팀 점유율 차이

import pandas as pd
import plotly.express as px

pos_df = pd.DataFrame({
    "리그":["EPL","Bundesliga","La Liga"],
    "승리팀":[53.43,51.67,53.91],
    "패배팀":[49.38,50.24,48.89]
})

plot_df = pos_df.melt(
    id_vars="리그",
    var_name="결과",
    value_name="점유율"
)

fig = px.bar(
    plot_df,
    x="리그",
    y="점유율",
    color="결과",
    barmode="group",
    text="점유율",
    title="승리팀 VS 패배팀 점유율 비교"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig.update_layout(
    yaxis=dict(range=[40,56]),
    title_x=0.5,
    width=900,
    height=600
)

fig.show()

# ============================================================
# 변수 4개 랜덤 포레스트

import pandas as pd
import plotly.express as px

rf_df = pd.DataFrame({
    "리그":["EPL","EPL","EPL","EPL",
              "Bundesliga","Bundesliga","Bundesliga","Bundesliga",
              "La Liga","La Liga","La Liga","La Liga"],
    "변수":["ShotOn","Corner","Foul","Possession"]*3,
    "중요도":[
        0.108,0.160,0.135,0.597,
        0.174,0.200,0.239,0.388,
        0.189,0.125,0.157,0.534
    ]
})

fig = px.bar(
    rf_df,
    x="중요도",
    y="변수",
    color="리그",
    orientation="h",
    barmode="group",
    text="중요도",
    title="리그별 경기 변수 중요도 비교 (랜덤 포레스트)"
)

fig.update_traces(
    texttemplate="%{text:.3f}",
    textposition="outside"
)

fig.update_layout(
    title_x=0.5,
    width=1000,
    height=600
)

fig.show()

# ============================================================

# 변수 3개 추가 버전 랜덤 포레스트(3개 리그 평균)
#home_win_rate → 해당 팀의 홈 경기 승률
#away_win_rate → 해당 팀의 원정 경기 승률
#win_rate_diff → 홈팀 승률 - 원정팀 승률

import pandas as pd
import plotly.express as px

rf_df=pd.DataFrame({
    "변수":[
        "ShotOn",
        "Corner",
        "Foul",
        "Possession",
        "Home Win Rate",
        "Away Win Rate",
        "Win Rate Diff"
    ],
    "중요도":[
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
    by="중요도",
    ascending=True
)

fig=px.bar(
    rf_df,
    x="중요도",
    y="변수",
    orientation="h",
    text="중요도",
    title="3개 리그 평균 변수 중요도(랜덤 포레스트)"
)

fig.update_traces(
    texttemplate="%{text:.3f}",
    textposition="outside"
)
fig.update_layout(
    xaxis_range=[0,0.38]
)

fig.show()
