import pandas as pd
from project.config import experiments_config
from utils.data import get_df
from evaluation.plots import plot_multiple, plot_one, bar_plot_with_moving_avg

def main():
    league_config = experiments_config.get("data").get("league")
    comparisons = league_config.get("comparisons")
    for comparison in comparisons:
        plot_league_data(comparison, league_config)

def plot_league_data(comparison, league_config):
    vis_path = league_config.get("vis_path")
    data_dir = league_config.get("dir")

    input_path = f"{data_dir}/{comparison}.csv"
    output_path = f"visualizations/{vis_path}/{comparison}.png"
    diff_output_path = f"visualizations/{vis_path}/diff/{comparison}.png"

    df = get_df(input_path)
    seasons = df["Season"].tolist()
    al_col = df["AL"].tolist()
    nl_col = df["NL"].tolist()

    diff = [al - nl for al, nl in zip(al_col, nl_col)]
    df = pd.DataFrame({"Season": seasons, "Difference": diff})
    df["MovingAvg"] = df["Difference"].rolling(window=3, center=True).mean()

    labels = ["AL", "NL"]
    all_y_vals = [al_col, nl_col]

    plot_multiple(
        x_vals=seasons,
        all_y_vals=all_y_vals,
        labels=labels,
        title=f"League Comparison: {comparison}",
        xlabel="Season",
        ylabel=comparison,
        save_path=output_path,
        display=False
    )

    '''plot_one(
        x_vals=seasons,
        y_vals=diff,
        title=f"League Difference (AL - NL): {comparison}",
        xlabel="Season",
        ylabel=f"{comparison} Difference",
        save_path=diff_output_path,
        display=False
    )'''

    bar_plot_with_moving_avg(
        x_vals=seasons,
        y_vals=diff,
        moving_avg=df["MovingAvg"],
        title=f"League Difference (AL - NL): {comparison}",
        xlabel="Season",
        ylabel=f"{comparison} Difference",
        save_path=diff_output_path
    )


if __name__ == "__main__":
    main()