import matplotlib.pyplot as plt
import seaborn as sns
from project.config import behavior_config
from utils.file_io import make_directory_for_file


def set_plot_params():
    plot_params = behavior_config.get('plot_params', {})

    figsize = plot_params.get('figure.figsize', (14, 8))
    figsize = tuple(figsize)
    plt.rcParams.update({
        'figure.figsize': figsize,
        **plot_params
    })

    plt.figure()


def plot_one(x_vals, y_vals, title="Plot", xlabel="X", ylabel="Y", save_path=None, display=False):
    set_plot_params()
    plt.plot(x_vals, y_vals, marker="o", linestyle="-")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if save_path:
        make_directory_for_file(save_path)
        plt.savefig(save_path)
    if display:
        plt.show()
    plt.close()


def plot_multiple(x_vals, all_y_vals, labels, title="Multiple Plot", xlabel="X", ylabel="Y", save_path=None, display=False):
    set_plot_params()
    for y_vals, label in zip(all_y_vals, labels):
        plt.plot(x_vals, y_vals, marker="o", linestyle="-", label=label)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.legend()

    if save_path:
        make_directory_for_file(save_path)
        plt.savefig(save_path)
    if display:
        plt.show()
    
    plt.clf()


def plot_heatmap(data, title, save_path=None):
    set_plot_params()

    sns.heatmap(data, cmap='coolwarm', center=0, square=True)
    plt.title(title)
    if save_path:
        make_directory_for_file(save_path)
        plt.savefig(save_path)
    plt.close()

def bar_plot_with_moving_avg(x_vals, y_vals, moving_avg, title, xlabel, ylabel, save_path):
    set_plot_params()

    plt.bar(x_vals, y_vals, label=ylabel, alpha=0.6, color="gray")

    plt.plot(x_vals, moving_avg, label=f"Moving Avg", linewidth=2, color="blue")

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)

    if save_path:
        make_directory_for_file(save_path)
        plt.savefig(save_path)
    plt.close()