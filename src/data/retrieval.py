import pandas as pd
from project.config import experiments_config, behavior_config
from utils.file_io import create_or_replace_csv, append_row_to_csv
from data.auth import make_auth_url, make_headers
from data.helpers import get_api_data
from pybaseball import team_batting, team_ids
from project.logger import logger
from utils.data import get_df, save_df

def main():
    data_config = experiments_config.get("data")

    team_batting_config = data_config.get("team_batting")
    save_team_batting_data(team_batting_config)

    league_config = data_config.get("league")
    save_league_avg_data(league_config, team_batting_config.get("dir"))

    pass

def save_team_batting_data(config):

    season_range = config.get("season_range")

    example_df = team_batting(2024)

    headers = example_df.columns.tolist()
    teams = get_team_ids_and_names()

    al_ids, nl_ids = get_al_nl_ids()

    numeric_headers = example_df.select_dtypes(include="number").columns.tolist()
    create_or_replace_csv(f"{config.get('dir')}/league_totals.csv", numeric_headers)
    create_or_replace_csv(f"{config.get('dir')}/al.csv", numeric_headers)
    create_or_replace_csv(f"{config.get('dir')}/nl.csv", numeric_headers)

    for team, name in teams:
        create_or_replace_csv(f"{config.get('dir')}/{name}.csv", headers)

    for year in range(season_range[0], season_range[1] + 1):
        season_data = team_batting(year)
        for team, name in teams:
            team_data = season_data[season_data["teamIDfg"] == team]
            if(team_data.empty):
                continue
            append_row_to_csv(f"{config.get('dir')}/{name}.csv", team_data.values.tolist()[0])
    
        league_row = season_data[numeric_headers].mean(numeric_only=True)
        al_row = season_data[season_data["teamIDfg"].isin(al_ids)][numeric_headers].mean(numeric_only=True)
        nl_row = season_data[season_data["teamIDfg"].isin(nl_ids)][numeric_headers].mean(numeric_only=True)

        append_row_to_csv(f"{config.get('dir')}/league_totals.csv", league_row)
        append_row_to_csv(f"{config.get('dir')}/al.csv", al_row)
        append_row_to_csv(f"{config.get('dir')}/nl.csv", nl_row)

def save_league_avg_data(league_config, team_batting_dir):
    al_df = get_df(f"{team_batting_dir}/al.csv")
    nl_df = get_df(f"{team_batting_dir}/nl.csv")

    dir = league_config.get("dir")
    comparisons = league_config.get("comparisons")
    for comparison in comparisons:
        file = f"{dir}/{comparison}.csv"
        seasons = al_df["Season"].tolist()
        al_col = al_df[comparison].tolist()
        nl_col = nl_df[comparison].tolist()

        out_df = pd.DataFrame({
            "Season": seasons,
            "AL": al_col,
            "NL": nl_col
        })

        save_df(out_df, file)

        out_df.to_csv(file, index=False)



    
def get_team_ids_and_names():
    example_df = team_batting(2024)

    teams = example_df["teamIDfg"].unique().tolist()
    names = example_df["Team"].unique().tolist()

    team_name = [[team, name] for team, name in zip(teams, names)]

    return team_name

def get_al_nl_ids():
    return team_ids(league="AL")["teamIDfg"].tolist(), team_ids(league="NL")["teamIDfg"].tolist()

if __name__ == "__main__":
    main()
