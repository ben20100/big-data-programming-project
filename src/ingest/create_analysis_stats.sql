CREATE TABLE analysis_stats AS
SELECT
    m.match_api_id,

    CAST(m.home_team_goal AS INT) AS home_goal,
    CAST(m.away_team_goal AS INT) AS away_goal,

    CAST(s.shoton AS INT) AS shoton,
    CAST(s.shotoff AS INT) AS shotoff,
    CAST(s.foulcommit AS INT) AS foulcommit,
    CAST(s.corner_stat AS INT) AS corner_stat,
    CAST(s.possession AS DOUBLE) AS possession,

    CASE
        WHEN CAST(m.home_team_goal AS INT)
             > CAST(m.away_team_goal AS INT)
        THEN 1
        ELSE 0
    END AS win

FROM matches m
JOIN match_stats s
ON m.match_api_id = s.match_api_id;
