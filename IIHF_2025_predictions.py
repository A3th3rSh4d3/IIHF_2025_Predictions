#%% Import Libraries
import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

#%% Constants and Configurations
DB_NAME = "iihf_2025_stats.db"
TOP_8_TEAMS = ["CZE", "SUI", "AUT", "CAN", "USA", "SWE", "DEN", "FIN"]
QUARTER_FINAL_MATCHUPS = [("USA", "FIN"), ("SUI", "AUT"), ("SWE", "CZE"), ("CAN", "DEN")]

#%% Data Definitions
# Team scoring efficiency data (all teams, later filtered to top 8)
team_data = [
    {"rnk": 1, "team": "CZE", "gp": 7, "gf": 35, "ssg": 177, "sog": 212, "sg%": 16.51},
    {"rnk": 2, "team": "SUI", "gp": 7, "gf": 34, "ssg": 184, "sog": 218, "sg%": 15.60},
    {"rnk": 3, "team": "AUT", "gp": 7, "gf": 21, "ssg": 130, "sog": 151, "sg%": 13.91},
    {"rnk": 4, "team": "CAN", "gp": 7, "gf": 34, "ssg": 241, "sog": 275, "sg%": 12.36},
    {"rnk": 5, "team": "USA", "gp": 7, "gf": 34, "ssg": 253, "sog": 287, "sg%": 11.85},
    {"rnk": 6, "team": "SWE", "gp": 7, "gf": 28, "ssg": 209, "sog": 237, "sg%": 11.81},
    {"rnk": 7, "team": "DEN", "gp": 7, "gf": 25, "ssg": 190, "sog": 215, "sg%": 11.63},
    {"rnk": 8, "team": "FIN", "gp": 7, "gf": 22, "ssg": 182, "sog": 204, "sg%": 10.78},
    {"rnk": 9, "team": "GER", "gp": 7, "gf": 20, "ssg": 166, "sog": 186, "sg%": 10.75},
    {"rnk": 10, "team": "LAT", "gp": 7, "gf": 17, "ssg": 159, "sog": 176, "sg%": 9.66},
    {"rnk": 11, "team": "SLO", "gp": 7, "gf": 9, "ssg": 105, "sog": 114, "sg%": 7.89},
    {"rnk": 12, "team": "NOR", "gp": 7, "gf": 13, "ssg": 154, "sog": 167, "sg%": 7.78},
    {"rnk": 13, "team": "HUN", "gp": 7, "gf": 8, "ssg": 99, "sog": 107, "sg%": 7.48},
    {"rnk": 14, "team": "KAZ", "gp": 7, "gf": 9, "ssg": 135, "sog": 144, "sg%": 6.25},
    {"rnk": 15, "team": "FRA", "gp": 7, "gf": 8, "ssg": 132, "sog": 140, "sg%": 5.71},
    {"rnk": 16, "team": "SVK", "gp": 7, "gf": 9, "ssg": 184, "sog": 193, "sg%": 4.66}
]

# Skater data (filtered for top 8 teams)
skater_data = [
    {"rnk": 1, "name": "PASTRNAK David", "pos": "F", "team": "CZE", "gp": 7, "g": 6, "a": 8, "pts": 14, "pim": 2, "+/-": 9},
    {"rnk": 2, "name": "MacKINNON Nathan", "pos": "F", "team": "CAN", "gp": 7, "g": 7, "a": 6, "pts": 13, "pim": 10, "+/-": 9},
    {"rnk": 3, "name": "CERVENKA Roman", "pos": "F", "team": "CZE", "gp": 7, "g": 5, "a": 8, "pts": 13, "pim": 4, "+/-": 11},
    {"rnk": 4, "name": "KONECNY Travis", "pos": "F", "team": "CAN", "gp": 7, "g": 3, "a": 9, "pts": 12, "pim": 10, "+/-": 9},
    {"rnk": 5, "name": "LINDHOLM Elias", "pos": "F", "team": "SWE", "gp": 7, "g": 7, "a": 4, "pts": 11, "pim": 0, "+/-": 6},
    {"rnk": 6, "name": "NAZAR Frank", "pos": "F", "team": "USA", "gp": 7, "g": 6, "a": 5, "pts": 11, "pim": 4, "+/-": 6},
    {"rnk": 7, "name": "CROSBY Sidney", "pos": "F", "team": "CAN", "gp": 7, "g": 4, "a": 7, "pts": 11, "pim": 6, "+/-": 7},
    {"rnk": 8, "name": "SEDLAK Lukas", "pos": "F", "team": "CZE", "gp": 7, "g": 4, "a": 5, "pts": 9, "pim": 0, "+/-": 11},
    {"rnk": 9, "name": "MOY Tyler", "pos": "F", "team": "SUI", "gp": 7, "g": 3, "a": 6, "pts": 9, "pim": 0, "+/-": 7},
    {"rnk": 9, "name": "OLESEN Nick", "pos": "F", "team": "DEN", "gp": 7, "g": 3, "a": 6, "pts": 9, "pim": 4, "+/-": -1},
    {"rnk": 11, "name": "KELLER Clayton", "pos": "F", "team": "USA", "gp": 7, "g": 2, "a": 7, "pts": 9, "pim": 0, "+/-": 1},
    {"rnk": 11, "name": "MONTOUR Brandon", "pos": "D", "team": "CAN", "gp": 7, "g": 2, "a": 7, "pts": 9, "pim": 0, "+/-": 5},
    {"rnk": 13, "name": "TERAVAINEN Teuvo", "pos": "F", "team": "FIN", "gp": 6, "g": 1, "a": 8, "pts": 9, "pim": 0, "+/-": 7},
    {"rnk": 14, "name": "MALGIN Denis", "pos": "F", "team": "SUI", "gp": 6, "g": 0, "a": 9, "pts": 9, "pim": 4, "+/-": 3},
    {"rnk": 15, "name": "ANDRIGHETTO Sven", "pos": "F", "team": "SUI", "gp": 6, "g": 7, "a": 1, "pts": 8, "pim": 0, "+/-": 4},
    {"rnk": 16, "name": "TOLVANEN Eeli", "pos": "F", "team": "FIN", "gp": 7, "g": 6, "a": 2, "pts": 8, "pim": 2, "+/-": 7},
    {"rnk": 17, "name": "HORVAT Bo", "pos": "F", "team": "CAN", "gp": 6, "g": 4, "a": 4, "pts": 8, "pim": 2, "+/-": 5},
    {"rnk": 18, "name": "COOLEY Logan", "pos": "F", "team": "USA", "gp": 7, "g": 4, "a": 4, "pts": 8, "pim": 8, "+/-": 2},
    {"rnk": 19, "name": "BLICHFELD Joachim", "pos": "F", "team": "DEN", "gp": 7, "g": 2, "a": 6, "pts": 8, "pim": 4, "+/-": 0},
    {"rnk": 19, "name": "RAYMOND Lucas", "pos": "F", "team": "SWE", "gp": 7, "g": 2, "a": 6, "pts": 8, "pim": 0, "+/-": 7},
    {"rnk": 21, "name": "FLEK Jakub", "pos": "F", "team": "CZE", "gp": 7, "g": 5, "a": 2, "pts": 7, "pim": 0, "+/-": 8},
    {"rnk": 21, "name": "THOMPSON Tage", "pos": "F", "team": "USA", "gp": 7, "g": 5, "a": 2, "pts": 7, "pim": 4, "+/-": 4},
    {"rnk": 23, "name": "GAUTHIER Cutter", "pos": "F", "team": "USA", "gp": 7, "g": 4, "a": 3, "pts": 7, "pim": 2, "+/-": 6},
    {"rnk": 23, "name": "KASPER Marco", "pos": "F", "team": "AUT", "gp": 7, "g": 4, "a": 3, "pts": 7, "pim": 2, "+/-": 8},
    {"rnk": 25, "name": "BRODIN Jonas", "pos": "D", "team": "SWE", "gp": 7, "g": 3, "a": 4, "pts": 7, "pim": 2, "+/-": 9},
    {"rnk": 25, "name": "LEHTONEN Mikko", "pos": "D", "team": "FIN", "gp": 7, "g": 3, "a": 4, "pts": 7, "pim": 2, "+/-": 8},
    {"rnk": 25, "name": "ZWERGER Dominic", "pos": "F", "team": "AUT", "gp": 7, "g": 3, "a": 4, "pts": 7, "pim": 8, "+/-": 7},
    {"rnk": 29, "name": "FIALA Kevin", "pos": "F", "team": "SUI", "gp": 5, "g": 2, "a": 5, "pts": 7, "pim": 4, "+/-": 8},
    {"rnk": 30, "name": "GARLAND Conor", "pos": "F", "team": "USA", "gp": 7, "g": 2, "a": 5, "pts": 7, "pim": 12, "+/-": 6},
    {"rnk": 30, "name": "MEIER Timo", "pos": "F", "team": "SUI", "gp": 7, "g": 2, "a": 5, "pts": 7, "pim": 4, "+/-": 10},
    {"rnk": 30, "name": "SCHNEIDER Peter", "pos": "F", "team": "AUT", "gp": 7, "g": 2, "a": 5, "pts": 7, "pim": 4, "+/-": 5}
]

# Goalkeeper data (filtered for top 8 teams)
goalkeeper_data = [
    {"rnk": 1, "name": "ERSSON Samuel", "team": "SWE", "gkd": 7, "gpi": 3, "mip": "179:24", "mip%": 43.20, "sog": 51, "ga": 2, "svs": 49, "svs%": 96.08, "gaa": 0.67, "ppga": 0, "shga": 0, "so": 2},
    {"rnk": 2, "name": "SAROS Juuse", "team": "FIN", "gkd": 6, "gpi": 5, "mip": "302:17", "mip%": 71.55, "sog": 147, "ga": 6, "svs": 141, "svs%": 95.92, "gaa": 1.19, "ppga": 1, "shga": 1, "so": 0},
    {"rnk": 3, "name": "VLADAR Daniel", "team": "CZE", "gkd": 7, "gpi": 3, "mip": "180:00", "mip%": 42.64, "sog": 62, "ga": 3, "svs": 59, "svs%": 95.16, "gaa": 1.00, "ppga": 0, "shga": 0, "so": 1},
    {"rnk": 4, "name": "BINNINGTON Jordan", "team": "CAN", "gkd": 5, "gpi": 3, "mip": "180:00", "mip%": 42.35, "sog": 57, "ga": 3, "svs": 54, "svs%": 94.74, "gaa": 1.00, "ppga": 1, "shga": 1, "so": 2},
    {"rnk": 5, "name": "FLEURY Marc-Andre", "team": "CAN", "gkd": 7, "gpi": 3, "mip": "185:00", "mip%": 43.53, "sog": 54, "ga": 3, "svs": 51, "svs%": 94.44, "gaa": 0.97, "ppga": 0, "shga": 0, "so": 0},
    {"rnk": 6, "name": "CHARLIN Stephane", "team": "SUI", "gkd": 7, "gpi": 3, "mip": "180:00", "mip%": 42.60, "sog": 43, "ga": 3, "svs": 40, "svs%": 93.02, "gaa": 1.00, "ppga": 0, "shga": 1, "so": 1},
    {"rnk": 8, "name": "GENONI Leonardo", "team": "SUI", "gkd": 6, "gpi": 4, "mip": "242:30", "mip%": 57.40, "sog": 80, "ga": 6, "svs": 74, "svs%": 92.50, "gaa": 1.48, "ppga": 3, "shga": 0, "so": 2},
    {"rnk": 9, "name": "KICKERT David", "team": "AUT", "gkd": 7, "gpi": 5, "mip": "309:25", "mip%": 72.28, "sog": 125, "ga": 10, "svs": 115, "svs%": 92.00, "gaa": 1.94, "ppga": 4, "shga": 0, "so": 0},
    {"rnk": 10, "name": "DACCORD Joey", "team": "USA", "gkd": 7, "gpi": 3, "mip": "180:00", "mip%": 42.44, "sog": 74, "ga": 6, "svs": 68, "svs%": 91.89, "gaa": 2.00, "ppga": 1, "shga": 0, "so": 1},
    {"rnk": 11, "name": "VEJMELKA Karel", "team": "CZE", "gkd": 7, "gpi": 4, "mip": "242:09", "mip%": 57.36, "sog": 120, "ga": 10, "svs": 110, "svs%": 91.67, "gaa": 2.48, "ppga": 4, "shga": 0, "so": 0},
    {"rnk": 13, "name": "MARKSTROM Jacob", "team": "SWE", "gkd": 6, "gpi": 4, "mip": "235:54", "mip%": 56.80, "sog": 67, "ga": 6, "svs": 61, "svs%": 91.04, "gaa": 1.53, "ppga": 0, "shga": 0, "so": 2},
    {"rnk": 15, "name": "DICHOW Frederik", "team": "DEN", "gkd": 7, "gpi": 6, "mip": "358:05", "mip%": 84.47, "sog": 164, "ga": 16, "svs": 148, "svs%": 90.24, "gaa": 2.68, "ppga": 2, "shga": 0, "so": 0},
    {"rnk": 18, "name": "SWAYMAN Jeremy", "team": "USA", "gkd": 7, "gpi": 4, "mip": "244:09", "mip%": 57.56, "sog": 75, "ga": 8, "svs": 67, "svs%": 89.33, "gaa": 1.97, "ppga": 3, "shga": 1, "so": 1}
]

#%% Create and Store DataFrames
def create_and_store_dataframes():
    """Create DataFrames and store them in SQLite and CSV."""
    # Team DataFrame
    df_teams = pd.DataFrame(team_data)
    df_teams = df_teams.astype({
        "rnk": "Int64", "team": str, "gp": "Int64", "gf": "Int64",
        "ssg": "Int64", "sog": "Int64", "sg%": float
    })
    df_playoffs = df_teams[df_teams["rnk"] <= 8].copy()
    
    # Skater DataFrame
    df_skaters = pd.DataFrame(skater_data)
    df_skaters = df_skaters.astype({
        "rnk": "Int64", "name": str, "pos": str, "team": str, "gp": "Int64",
        "g": "Int64", "a": "Int64", "pts": "Int64", "pim": "Int64", "+/-": "Int64"
    })
    df_skaters_playoffs = df_skaters[df_skaters["team"].isin(TOP_8_TEAMS)].copy()
    
    # Goalkeeper DataFrame
    df_goalkeepers = pd.DataFrame(goalkeeper_data)
    df_goalkeepers = df_goalkeepers.astype({
        "rnk": "Int64", "name": str, "team": str, "gkd": "Int64", "gpi": "Int64",
        "mip": str, "mip%": float, "sog": "Int64", "ga": "Int64", "svs": "Int64",
        "svs%": float, "gaa": float, "ppga": "Int64", "shga": "Int64", "so": "Int64"
    })
    
    # Save to CSV
    df_playoffs.to_csv("iihf_scoring_efficiency_playoffs.csv", index=False)
    df_skaters_playoffs.to_csv("iihf_skaters_playoffs.csv", index=False)
    df_goalkeepers.to_csv("iihf_goalkeepers_playoffs.csv", index=False)
    
    # Save to SQLite
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # Team table
        cursor.execute("DROP TABLE IF EXISTS scoring_efficiency_playoffs")
        cursor.execute("""
            CREATE TABLE scoring_efficiency_playoffs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rnk INTEGER, team TEXT, gp INTEGER, gf INTEGER,
                ssg INTEGER, sog INTEGER, sg_pct REAL
            )
        """)
        df_playoffs.rename(columns={"sg%": "sg_pct"}).to_sql(
            "scoring_efficiency_playoffs", conn, if_exists="append", index=False
        )
        
        # Skater table
        cursor.execute("DROP TABLE IF EXISTS skaters_playoffs")
        cursor.execute("""
            CREATE TABLE skaters_playoffs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rnk INTEGER, name TEXT, pos TEXT, team TEXT,
                gp INTEGER, g INTEGER, a INTEGER, pts INTEGER,
                pim INTEGER, plus_minus INTEGER
            )
        """)
        df_skaters_playoffs.rename(columns={"+/-": "plus_minus"}).to_sql(
            "skaters_playoffs", conn, if_exists="append", index=False
        )
        
        # Goalkeeper table
        cursor.execute("DROP TABLE IF EXISTS goalkeepers_playoffs")
        cursor.execute("""
            CREATE TABLE goalkeepers_playoffs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rnk INTEGER, name TEXT, team TEXT, gkd INTEGER,
                gpi INTEGER, mip TEXT, mip_pct REAL, sog INTEGER,
                ga INTEGER, svs INTEGER, svs_pct REAL, gaa REAL,
                ppga INTEGER, shga INTEGER, so INTEGER
            )
        """)
        df_goalkeepers.rename(columns={"mip%": "mip_pct", "svs%": "svs_pct"}).to_sql(
            "goalkeepers_playoffs", conn, if_exists="append", index=False
        )
    
    print(f"DataFrames saved to CSV and SQLite database: {DB_NAME}")
    return df_playoffs, df_skaters_playoffs, df_goalkeepers

#%% Calculate Team Metrics
def calculate_team_metrics(df_playoffs, df_skaters_playoffs, df_goalkeepers_playoffs):
    """Calculate offensive, defensive, and depth metrics for each team."""
    team_metrics = []
    for team in df_playoffs["team"]:
        team_data = df_playoffs[df_playoffs["team"] == team]
        skaters = df_skaters_playoffs[df_skaters_playoffs["team"] == team]
        goalkeepers = df_goalkeepers_playoffs[df_goalkeepers_playoffs["team"] == team]
        
        # Offensive metrics
        gf = team_data["gf"].iloc[0]
        sg_pct = team_data["sg%"].iloc[0]
        top_skaters = skaters.nlargest(5, "pts")
        avg_pts_per_game = top_skaters["pts"].sum() / top_skaters["gp"].sum() if len(top_skaters) > 0 else 0
        
        # Defensive metrics
        avg_svs_pct = goalkeepers["svs%"].mean() if len(goalkeepers) > 0 else 0
        avg_gaa = goalkeepers["gaa"].mean() if len(goalkeepers) > 0 else 5
        inv_gaa = 1 / avg_gaa if avg_gaa > 0 else 0
        
        # Depth
        depth = len(skaters[skaters["pts"] >= 7])
        
        team_metrics.append({
            "team": team, "gf": gf, "sg%": sg_pct, "avg_pts_per_game": avg_pts_per_game,
            "avg_svs%": avg_svs_pct, "inv_gaa": inv_gaa, "depth": depth
        })
    
    df_metrics = pd.DataFrame(team_metrics)
    
    # Normalize metrics
    for col in ["gf", "sg%", "avg_pts_per_game", "avg_svs%", "inv_gaa", "depth"]:
        df_metrics[col] = (df_metrics[col] - df_metrics[col].min()) / (df_metrics[col].max() - df_metrics[col].min())
    
    # Calculate scores
    df_metrics["offense_score"] = 0.4 * df_metrics["gf"] + 0.3 * df_metrics["sg%"] + 0.3 * df_metrics["avg_pts_per_game"]
    df_metrics["defense_score"] = 0.5 * df_metrics["avg_svs%"] + 0.5 * df_metrics["inv_gaa"]
    df_metrics["overall_score"] = 0.5 * df_metrics["offense_score"] + 0.4 * df_metrics["defense_score"] + 0.1 * df_metrics["depth"]
    df_metrics["overall_score"] = 100 * df_metrics["overall_score"] / df_metrics["overall_score"].max()
    
    return df_metrics

#%% Simulate Playoff Bracket
def simulate_playoffs(df_metrics, matchups):
    """Simulate quarter-finals, semi-finals, and finals to predict medalists."""
    print("\nQuarter-Final Results:")
    qf_winners = []
    for team1, team2 in matchups:
        score1 = df_metrics[df_metrics["team"] == team1]["overall_score"].iloc[0]
        score2 = df_metrics[df_metrics["team"] == team2]["overall_score"].iloc[0]
        prob1 = 1 / (1 + np.exp(-(score1 - score2) / 10))
        winner = team1 if prob1 > 0.5 else team2
        qf_winners.append(winner)
        print(f"{team1} vs {team2}: {winner} wins (Prob: {prob1:.2f})")
    
    # Semi-finals (reseed by overall score)
    print("\nSemi-Final Results:")
    qf_winners_scores = df_metrics[df_metrics["team"].isin(qf_winners)][["team", "overall_score"]]
    qf_winners_scores = qf_winners_scores.sort_values("overall_score", ascending=False)
    sf_matchups = [
        (qf_winners_scores.iloc[0]["team"], qf_winners_scores.iloc[3]["team"]),
        (qf_winners_scores.iloc[1]["team"], qf_winners_scores.iloc[2]["team"])
    ]
    
    sf_winners = []
    sf_losers = []
    for team1, team2 in sf_matchups:
        score1 = df_metrics[df_metrics["team"] == team1]["overall_score"].iloc[0]
        score2 = df_metrics[df_metrics["team"] == team2]["overall_score"].iloc[0]
        prob1 = 1 / (1 + np.exp(-(score1 - score2) / 10))
        winner = team1 if prob1 > 0.5 else team2
        loser = team2 if prob1 > 0.5 else team1
        sf_winners.append(winner)
        sf_losers.append(loser)
        print(f"{team1} vs {team2}: {winner} wins (Prob: {prob1:.2f})")
    
    # Finals
    print("\nFinal Results:")
    # Gold medal game
    team1, team2 = sf_winners
    score1 = df_metrics[df_metrics["team"] == team1]["overall_score"].iloc[0]
    score2 = df_metrics[df_metrics["team"] == team2]["overall_score"].iloc[0]
    prob1 = 1 / (1 + np.exp(-(score1 - score2) / 10))
    gold = team1 if prob1 > 0.5 else team2
    silver = team2 if prob1 > 0.5 else team1
    print(f"Gold Medal Game: {team1} vs {team2}: {gold} wins (Prob: {prob1:.2f})")
    
    # Bronze medal game
    team1, team2 = sf_losers
    score1 = df_metrics[df_metrics["team"] == team1]["overall_score"].iloc[0]
    score2 = df_metrics[df_metrics["team"] == team2]["overall_score"].iloc[0]
    prob1 = 1 / (1 + np.exp(-(score1 - score2) / 10))
    bronze = team1 if prob1 > 0.5 else team2
    print(f"Bronze Medal Game: {team1} vs {team2}: {bronze} wins (Prob: {prob1:.2f})")
    
    return gold, silver, bronze, df_metrics

#%% Create Visualization
def create_visualization(df_playoffs, df_goalkeepers_playoffs):
    """Create a bar plot comparing GF, SOG, and average SVS% for top 8 teams."""
    df_plot = df_playoffs[["team", "gf", "sog"]].copy()
    avg_svs = df_goalkeepers_playoffs.groupby("team")["svs%"].mean().reset_index()
    df_plot = df_plot.merge(avg_svs, on="team")
    
    # Scale SOG and SVS% to GF range for visualization
    df_plot["sog_scaled"] = df_plot["sog"] * (df_plot["gf"].max() / df_plot["sog"].max())
    df_plot["svs_scaled"] = df_plot["svs%"] * (df_plot["gf"].max() / df_plot["svs%"].max())
    
    # Create grouped bar plot
    fig, ax = plt.subplots(figsize=(12, 6))
    bar_width = 0.25
    x = np.arange(len(df_plot["team"]))
    
    ax.bar(x - bar_width, df_plot["gf"], bar_width, label="Goals For (GF)", color="#1f77b4")
    ax.bar(x, df_plot["sog_scaled"], bar_width, label="Shots on Goal (Scaled)", color="#ff7f0e")
    ax.bar(x + bar_width, df_plot["svs_scaled"], bar_width, label="Avg Goalkeeper SVS% (Scaled)", color="#2ca02c")
    
    ax.set_xlabel("Team", fontsize=12)
    ax.set_ylabel("Metrics (Scaled to GF Range)", fontsize=12)
    ax.set_title("IIHF 2025 Top 8 Teams: Offensive and Defensive Strengths", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(df_plot["team"], rotation=45, fontsize=10)
    ax.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig("iihf_team_comparison.png", dpi=300)
    plt.show()

#%% Main Execution
def main():
    """Main function to process data, predict medalists, and visualize results."""
    # Create and store DataFrames
    df_playoffs, df_skaters_playoffs, df_goalkeepers_playoffs = create_and_store_dataframes()
    
    # Calculate team metrics
    df_metrics = calculate_team_metrics(df_playoffs, df_skaters_playoffs, df_goalkeepers_playoffs)
    
    # Simulate playoffs
    gold, silver, bronze, df_metrics = simulate_playoffs(df_metrics, QUARTER_FINAL_MATCHUPS)
    
    # Create visualization and display predictions
    print("\nFinal Medal Predictions:")
    print(f"Gold: {gold}")
    print(f"Silver: {silver}")
    print(f"Bronze: {bronze}")
    
    print("\nTeam Metrics:")
    print(df_metrics[["team", "offense_score", "defense_score", "depth", "overall_score"]].round(2))
    
    create_visualization(df_playoffs, df_goalkeepers_playoffs)

if __name__ == "__main__":
    main()